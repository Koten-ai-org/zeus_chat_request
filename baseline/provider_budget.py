"""Shared LLM budget for the beer and travel runtimes.

Both scopes use one API key, so they share one gate. The gate reserves an
estimate, sleeps until a 60-second window can hold it, then replaces the
estimate with the provider usage when that comes back.

A request larger than the per-request cap or the whole per-minute token cap
cannot be fixed by waiting. ``BudgetExceeded`` is that case. The caller
stops both scopes. This module does not shrink the prompt.

Token estimate matches the report ``tk``: UTF-8 bytes divided by 4, rounded
up. It is not the model's tokenizer. Published numbers and the code caps
are listed in ``baseline/README.md``.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

# 80 percent of a published number, rounded down, at least 1.
# Env overrides are not passed through this. The harness floor is not either.
def headroom(published: int) -> int:
    return max(1, published * 4 // 5)


# Used only when the provider does not publish one RPM and one TPM this
# script can apply. Already the enforced ceiling. Do not run it through headroom.
FLOOR_RPM = 60
FLOOR_TPM = 100_000

# Added to the prompt estimate when the request does not set max_tokens.
# xAI counts completion and reasoning tokens toward TPM.
COMPLETION_RESERVE = 1024

WINDOW_S = 60.0

# Tier 0 on https://docs.x.ai/developers/rate-limits (RPS, TPM).
# Any other xAI model id uses the grok-4.7 row. That is a code choice.
_XAI_TIER0 = (
    ("grok-4.20-multi-agent", 9, 2_500_000),
    ("grok-4.3", 37, 10_000_000),
    ("grok-4.20", 37, 10_000_000),
    ("grok-build-0.1", 37, 10_000_000),
    ("grok-4.7", 150, 50_000_000),
    ("grok-4.6", 150, 50_000_000),
    ("grok-4.5", 150, 50_000_000),
)
_XAI_DEFAULT = (150, 50_000_000)

# Developer-plan base for openai/gpt-oss-120b on
# https://console.groq.com/docs/rate-limits . Applied to every Groq model id.
_GROQ_RPM = 30
_GROQ_TPM = 8_000

# Free-trial uncached TPM on https://inference-docs.cerebras.ai/support/rate-limits
_CEREBRAS_RPM = 5
_CEREBRAS_TPM = 30_000

# https://openrouter.ai/docs/api-reference/limits — ids ending in :free.
_OPENROUTER_FREE_RPM = 20


class BudgetExceeded(Exception):
    """Waiting cannot fit this request. The prompt was not changed."""


class BudgetConfigError(ValueError):
    """LLM_TPM, LLM_RPM, LLM_RPS, or LLM_REQUEST_TOKENS is not a whole number."""


@dataclass(frozen=True, slots=True)
class BudgetLimits:
    provider: str
    model: str
    rpm: int | None
    tpm: int | None
    rps: int | None
    request_tokens: int | None
    source: str

    def pace_line(self) -> str:
        return (
            f"pace provider={self.provider} model={self.model or '-'} "
            f"rps={_fmt(self.rps)} rpm={_fmt(self.rpm)} tpm={_fmt(self.tpm)} "
            f"request_tokens={_fmt(self.request_tokens)} source={self.source}"
        )


def _fmt(value: int | None) -> str:
    if value is None:
        return "-"
    return str(value)


def tokens_from_bytes(nbytes: int) -> int:
    """Same rule as report_bundle._tokens_from_bytes and the pack viewer."""
    if nbytes <= 0:
        return 0
    return max(1, (nbytes + 3) // 4)


def _json_tokens(payload: object) -> int:
    raw = json.dumps(payload, ensure_ascii=False, default=str, separators=(",", ":"))
    return tokens_from_bytes(len(raw.encode("utf-8")))


def estimate_prompt(req: Any) -> int:
    messages = getattr(req, "messages", ()) or ()
    tools = getattr(req, "tools", ()) or ()
    return _json_tokens({"messages": list(messages), "tools": list(tools)})


def completion_reserve(req: Any) -> int:
    max_tokens = getattr(req, "max_tokens", None)
    if isinstance(max_tokens, int) and not isinstance(max_tokens, bool) and max_tokens > 0:
        return max_tokens
    return COMPLETION_RESERVE


def estimate_request(req: Any) -> int:
    return estimate_prompt(req) + completion_reserve(req)


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value >= 0:
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def usage_total(usage: Mapping[str, Any] | None) -> int | None:
    """Prompt plus completion, or total_tokens when that is larger.

    Cached tokens are not subtracted. A provider that still bills them
    against TPM keeps them inside prompt_tokens.
    """
    if not isinstance(usage, Mapping) or not usage:
        return None
    prompt = _as_int(usage.get("prompt_tokens"))
    completion = _as_int(usage.get("completion_tokens"))
    total: int | None = None
    if prompt is not None or completion is not None:
        total = (prompt or 0) + (completion or 0)
    reported = _as_int(usage.get("total_tokens"))
    if reported is not None and (total is None or reported > total):
        total = reported
    if total is None:
        return None
    return max(0, total)


def _optional_int(env: Mapping[str, str], key: str) -> int | None:
    raw = env.get(key)
    if raw is None:
        return None
    text = str(raw).strip()
    if text == "":
        return None
    try:
        value = int(text)
    except ValueError as exc:
        raise BudgetConfigError(
            f"{key} must be a whole number, or unset. "
            "Zero blocks that dimension. It does not mean unlimited."
        ) from exc
    if value < 0:
        raise BudgetConfigError(
            f"{key} must be zero or greater. Zero blocks that dimension. Unset uses the README code column."
        )
    return value


def _xai_published(model: str) -> tuple[int, int]:
    name = model.strip().lower()
    for prefix, rps, tpm in _XAI_TIER0:
        if name.startswith(prefix):
            return rps, tpm
    return _XAI_DEFAULT


def _apply_env(limits: BudgetLimits, env: Mapping[str, str]) -> BudgetLimits:
    rpm = _optional_int(env, "LLM_RPM")
    tpm = _optional_int(env, "LLM_TPM")
    rps = _optional_int(env, "LLM_RPS")
    request_tokens = _optional_int(env, "LLM_REQUEST_TOKENS")
    used = [rpm, tpm, rps, request_tokens]
    if all(value is None for value in used):
        return limits
    source = limits.source if limits.source.endswith("+env") else f"{limits.source}+env"
    return BudgetLimits(
        provider=limits.provider,
        model=limits.model,
        rpm=limits.rpm if rpm is None else rpm,
        tpm=limits.tpm if tpm is None else tpm,
        rps=limits.rps if rps is None else rps,
        request_tokens=limits.request_tokens if request_tokens is None else request_tokens,
        source=source,
    )


def limits_for(provider: str, model: str, env: Mapping[str, str] | None = None) -> BudgetLimits:
    """Code cap for this provider and model. Env values replace one dimension.

    An env value is the script ceiling. It is not reduced by the 80 percent
    headroom a second time. Zero is a real ceiling.
    """
    name = (provider or "").strip().lower()
    model_id = (model or "").strip()
    env = env or {}
    if name == "xai":
        rps, tpm = _xai_published(model_id)
        base = BudgetLimits(name, model_id, None, headroom(tpm), headroom(rps), None, "xai-tier0-80pct")
    elif name == "groq":
        base = BudgetLimits(
            name, model_id, headroom(_GROQ_RPM), headroom(_GROQ_TPM), None, None, "groq-docs-80pct"
        )
    elif name == "cerebras":
        base = BudgetLimits(
            name,
            model_id,
            headroom(_CEREBRAS_RPM),
            headroom(_CEREBRAS_TPM),
            None,
            None,
            "cerebras-free-80pct",
        )
    elif name == "openrouter" and model_id.lower().endswith(":free"):
        base = BudgetLimits(
            name, model_id, headroom(_OPENROUTER_FREE_RPM), None, None, None, "openrouter-free-80pct"
        )
    elif name == "deepseek":
        # Concurrency only. Two scopes sit under that cap. Do not invent a TPM.
        base = BudgetLimits(name, model_id, None, None, None, None, "deepseek-concurrency")
    else:
        base = BudgetLimits(name or "unknown", model_id, FLOOR_RPM, FLOOR_TPM, None, None, "code-floor")
    return _apply_env(base, env)


@dataclass(slots=True)
class _Spend:
    at: float
    tokens: int
    ident: int


class ProviderBudget:
    """One sliding 60-second window, shared by every runtime in the process."""

    def __init__(
        self,
        limits: BudgetLimits,
        *,
        clock=None,
        sleep=None,
        log_waits: bool = True,
    ) -> None:
        self.limits = limits
        self._clock = clock or time.monotonic
        self._sleep = sleep or asyncio.sleep
        self._log_waits = log_waits
        self._lock = asyncio.Lock()
        self._changed = asyncio.Event()
        self._events: list[_Spend] = []
        self._seq = 0

    def pace_line(self) -> str:
        return self.limits.pace_line()

    def tokens_held(self) -> int:
        now = self._clock()
        return sum(event.tokens for event in self._events if now - event.at < WINDOW_S)

    def _live(self, now: float) -> list[_Spend]:
        return [event for event in self._events if now - event.at < WINDOW_S]

    def _refuse(self, tokens: int) -> None:
        limits = self.limits
        if limits.request_tokens is not None and tokens > limits.request_tokens:
            raise BudgetExceeded(
                f"estimated {tokens} tokens is over the per-request cap of {limits.request_tokens}"
            )
        if limits.tpm is not None and tokens > limits.tpm:
            raise BudgetExceeded(
                f"estimated {tokens} tokens is over the per-minute cap of {limits.tpm}"
            )
        if limits.rpm == 0:
            raise BudgetExceeded("LLM_RPM is 0, so no request can be sent")
        if limits.rps == 0:
            raise BudgetExceeded("LLM_RPS is 0, so no request can be sent")

    def _delay(self, now: float, tokens: int) -> float:
        delay = 0.0
        live = self._live(now)
        if self.limits.rps is not None and self.limits.rps > 0 and live:
            interval = 1.0 / self.limits.rps
            delay = max(delay, live[-1].at + interval - now)
        if self.limits.rpm is not None and self.limits.rpm > 0 and len(live) >= self.limits.rpm:
            delay = max(delay, live[0].at + WINDOW_S - now)
        if self.limits.tpm is not None and self.limits.tpm > 0:
            used = sum(event.tokens for event in live)
            if used + tokens > self.limits.tpm:
                need = used + tokens - self.limits.tpm
                freed = 0
                for event in live:
                    freed += event.tokens
                    if freed >= need:
                        delay = max(delay, event.at + WINDOW_S - now)
                        break
        if delay < 0:
            return 0.0
        return delay

    async def acquire(self, tokens: int) -> int:
        """Reserve ``tokens``. Return an id ``correct`` later uses.

        Sleeps outside the lock. A request that can never fit raises
        ``BudgetExceeded`` before any sleep.
        """
        self._refuse(tokens)
        if self.limits.rpm is None and self.limits.tpm is None and self.limits.rps is None:
            return 0
        while True:
            async with self._lock:
                now = self._clock()
                self._events = self._live(now)
                delay = self._delay(now, tokens)
                if delay <= 0:
                    self._seq += 1
                    self._events.append(_Spend(now, tokens, self._seq))
                    return self._seq
                self._changed.clear()
            started = self._clock()
            await self._wait(delay)
            waited = self._clock() - started
            if self._log_waits and waited >= 1.0:
                print(
                    f"pace wait {waited:.1f}s provider={self.limits.provider} "
                    f"tokens={tokens} tpm={_fmt(self.limits.tpm)} rpm={_fmt(self.limits.rpm)}",
                    flush=True,
                )

    async def _wait(self, delay: float) -> None:
        """Sleep, or return early when a usage correction frees room.

        Tests pass their own sleep so a fake clock can jump the window.
        The real clock waits on ``_changed`` and wakes when ``correct`` runs.
        """
        if self._sleep is not asyncio.sleep:
            await self._sleep(delay)
            return
        try:
            await asyncio.wait_for(self._changed.wait(), timeout=delay)
        except TimeoutError:
            return

    async def correct(self, ident: int, actual: int) -> None:
        """Replace a reservation with the tokens the provider reported."""
        if ident <= 0:
            return
        actual = max(0, actual)
        async with self._lock:
            for event in self._events:
                if event.ident == ident:
                    event.tokens = actual
                    break
        self._changed.set()


def budget_for(provider: str, model: str, env: Mapping[str, str] | None = None) -> ProviderBudget:
    return ProviderBudget(limits_for(provider, model, env))


class PacedLlm:
    """Wraps the OpenAI-compatible client. Attribute lookup falls through."""

    __slots__ = ("_inner", "_budget")

    def __init__(self, inner: Any, budget: ProviderBudget) -> None:
        self._inner = inner
        self._budget = budget

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    async def complete(self, req: Any) -> Any:
        reserved = estimate_request(req)
        ident = await self._budget.acquire(reserved)
        try:
            response = await self._inner.complete(req)
        except BaseException:
            await self._budget.correct(ident, estimate_prompt(req))
            raise
        actual = usage_total(getattr(response, "usage", None))
        await self._budget.correct(ident, reserved if actual is None else actual)
        return response


def self_check() -> int:
    """No network. Oversize raises, a full window sleeps, usage shrinks the ledger."""
    if tokens_from_bytes(0) != 0 or tokens_from_bytes(4) != 1 or tokens_from_bytes(5) != 2:
        print("provider budget token rule failed")
        return 1
    if headroom(150) != 120 or headroom(50_000_000) != 40_000_000:
        print("provider budget headroom failed")
        return 1
    if headroom(37) != 29 or headroom(9) != 7 or headroom(2_500_000) != 2_000_000:
        print("provider budget xai headroom failed")
        return 1
    grok = limits_for("xai", "grok-4.7", {})
    if grok.rps != 120 or grok.tpm != 40_000_000 or grok.rpm is not None or grok.request_tokens is not None:
        print("provider budget xai grok-4.7 failed", grok)
        return 1
    mid = limits_for("xai", "grok-4.20-0309-reasoning", {})
    if mid.rps != 29 or mid.tpm != 8_000_000:
        print("provider budget xai mid failed", mid)
        return 1
    low = limits_for("xai", "grok-4.20-multi-agent-0309", {})
    if low.rps != 7 or low.tpm != 2_000_000:
        print("provider budget xai multi-agent failed", low)
        return 1
    if limits_for("xai", "grok-4.3", {}).tpm != 8_000_000:
        print("provider budget xai 4.3 failed")
        return 1
    groq = limits_for("groq", "openai/gpt-oss-120b", {})
    if groq.rpm != 24 or groq.tpm != 6_400:
        print("provider budget groq failed", groq)
        return 1
    cerebras = limits_for("cerebras", "gpt-oss-120b", {})
    if cerebras.rpm != 4 or cerebras.tpm != 24_000:
        print("provider budget cerebras failed", cerebras)
        return 1
    deepseek = limits_for("deepseek", "deepseek-flash", {})
    if deepseek.rpm is not None or deepseek.tpm is not None or deepseek.rps is not None:
        print("provider budget deepseek invented a cap", deepseek)
        return 1
    free = limits_for("openrouter", "meta/llama:free", {})
    if free.rpm != 16 or free.tpm is not None:
        print("provider budget openrouter free failed", free)
        return 1
    paid = limits_for("openrouter", "meta/llama", {})
    if paid.rpm != FLOOR_RPM or paid.tpm != FLOOR_TPM or paid.source != "code-floor":
        print("provider budget openrouter paid failed", paid)
        return 1
    floor = limits_for("openai", "gpt-4.1", {})
    if floor.rpm != FLOOR_RPM or floor.tpm != FLOOR_TPM or floor.source != "code-floor":
        print("provider budget floor failed", floor)
        return 1
    if limits_for("ollama", "llama", {}).source != "code-floor":
        print("provider budget unknown floor failed")
        return 1
    overridden = limits_for("xai", "grok-4.7", {"LLM_TPM": "1000", "LLM_RPS": "3"})
    if overridden.tpm != 1000 or overridden.rps != 3 or overridden.rpm is not None:
        print("provider budget env was shrunk", overridden)
        return 1
    if not overridden.source.endswith("+env"):
        print("provider budget env source failed", overridden)
        return 1
    partial = limits_for("groq", "openai/gpt-oss-120b", {"LLM_RPM": "10"})
    if partial.rpm != 10 or partial.tpm != 6_400:
        print("provider budget partial env failed", partial)
        return 1
    if limits_for("openai", "gpt", {"LLM_TPM": "0"}).tpm != 0:
        print("provider budget zero became unlimited")
        return 1
    try:
        limits_for("xai", "grok-4.7", {"LLM_TPM": "nope"})
    except BudgetConfigError:
        pass
    else:
        print("provider budget bad env was accepted")
        return 1
    if usage_total({"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12}) != 12:
        print("provider budget usage sum failed")
        return 1
    if usage_total({"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 20}) != 20:
        print("provider budget usage total failed")
        return 1
    if usage_total({"prompt_tokens": 8, "prompt_tokens_details": {"cached_tokens": 8}}) != 8:
        print("provider budget cached tokens were subtracted")
        return 1
    if usage_total({}) is not None:
        print("provider budget empty usage failed")
        return 1
    line = grok.pace_line()
    if "provider=xai" not in line or "tpm=40000000" not in line or "rps=120" not in line:
        print("provider budget pace line failed", line)
        return 1

    class _Req:
        def __init__(self, content: str, max_tokens: int | None = None) -> None:
            self.messages = ({"role": "user", "content": content},)
            self.tools = ()
            self.max_tokens = max_tokens

    class _Resp:
        def __init__(self, usage: dict) -> None:
            self.usage = usage

    class _Inner:
        def __init__(self) -> None:
            self.calls = 0

        async def complete(self, req: _Req) -> _Resp:
            self.calls += 1
            return _Resp({"prompt_tokens": 4, "completion_tokens": 1})

    async def exercise() -> str | None:
        now = {"t": 0.0}
        slept: list[float] = []

        def clock() -> float:
            return now["t"]

        async def sleep(seconds: float) -> None:
            slept.append(seconds)
            now["t"] += seconds

        over = ProviderBudget(
            BudgetLimits("t", "m", None, 100, None, 50, "test"),
            clock=clock,
            sleep=sleep,
            log_waits=False,
        )
        try:
            await over.acquire(51)
        except BudgetExceeded:
            pass
        else:
            return "oversize request was sent"
        if slept or over.tokens_held():
            return "oversize request slept or reserved"
        try:
            await over.acquire(101)
        except BudgetExceeded:
            pass
        else:
            return "over-tpm request was sent"

        window = ProviderBudget(
            BudgetLimits("t", "m", 1, 1000, None, None, "test"),
            clock=clock,
            sleep=sleep,
            log_waits=False,
        )
        first = await window.acquire(80)
        await window.correct(first, 10)
        if window.tokens_held() != 10:
            return f"usage correction left {window.tokens_held()}"
        await window.acquire(10)
        if not slept or slept[-1] < 59:
            return f"full window did not sleep: {slept}"

        inner = _Inner()
        tight = ProviderBudget(
            BudgetLimits("t", "m", None, 10, None, None, "test"),
            clock=clock,
            sleep=sleep,
            log_waits=False,
        )
        paced = PacedLlm(inner, tight)
        try:
            await paced.complete(_Req("hello"))
        except BudgetExceeded:
            pass
        else:
            return "paced client sent an oversize request"
        if inner.calls != 0:
            return "inner client ran after a refusal"

        shared_limits = BudgetLimits("t", "m", None, 1_000_000, None, None, "test")
        shared = ProviderBudget(shared_limits, clock=clock, sleep=sleep, log_waits=False)
        left = PacedLlm(inner, shared)
        right = PacedLlm(inner, shared)
        await left.complete(_Req("hi"))
        await right.complete(_Req("hi"))
        if inner.calls != 2 or shared.tokens_held() != 10:
            return f"shared usage ledger failed calls={inner.calls} held={shared.tokens_held()}"

        class _Boom:
            async def complete(self, req: _Req) -> _Resp:
                raise RuntimeError("down")

        class _NoUsage:
            async def complete(self, req: _Req) -> _Resp:
                return _Resp({})

        failed_budget = ProviderBudget(
            BudgetLimits("t", "m", None, 1_000_000, None, None, "test"),
            clock=clock,
            sleep=sleep,
            log_waits=False,
        )
        sample = _Req("hi")
        try:
            await PacedLlm(_Boom(), failed_budget).complete(sample)
        except RuntimeError:
            pass
        else:
            return "failed model call was swallowed"
        if failed_budget.tokens_held() != estimate_prompt(sample):
            return f"failed call held {failed_budget.tokens_held()}"
        quiet = ProviderBudget(
            BudgetLimits("t", "m", None, 1_000_000, None, None, "test"),
            clock=clock,
            sleep=sleep,
            log_waits=False,
        )
        await PacedLlm(_NoUsage(), quiet).complete(sample)
        if quiet.tokens_held() != estimate_request(sample):
            return f"missing usage held {quiet.tokens_held()}"

        early = ProviderBudget(
            BudgetLimits("t", "m", None, 100, None, None, "test"),
            log_waits=False,
        )
        held = await early.acquire(80)
        waiter = asyncio.create_task(early.acquire(30))
        await asyncio.sleep(0.05)
        await early.correct(held, 10)
        try:
            await asyncio.wait_for(waiter, timeout=2)
        except TimeoutError:
            return "usage correction did not wake the waiting request"

        rps_now = {"t": 1000.0}
        rps_slept: list[float] = []

        def rps_clock() -> float:
            return rps_now["t"]

        async def rps_sleep(seconds: float) -> None:
            rps_slept.append(seconds)
            rps_now["t"] += seconds

        per_second = ProviderBudget(
            BudgetLimits("t", "m", None, None, 2, None, "test"),
            clock=rps_clock,
            sleep=rps_sleep,
            log_waits=False,
        )
        await per_second.acquire(1)
        await per_second.acquire(1)
        if not rps_slept or abs(rps_slept[-1] - 0.5) > 0.001:
            return f"rps interval did not sleep 0.5s: {rps_slept}"

        blocked = ProviderBudget(
            BudgetLimits("t", "m", 0, None, None, None, "test"),
            clock=clock,
            sleep=sleep,
            log_waits=False,
        )
        try:
            await blocked.acquire(1)
        except BudgetExceeded:
            pass
        else:
            return "rpm 0 was treated as unlimited"
        return None

    failed = asyncio.run(exercise())
    if failed:
        print("provider budget check failed:", failed)
        return 1
    print("provider budget check ok")
    return 0
