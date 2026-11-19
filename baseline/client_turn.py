"""Drive one A/B question through zeus_client's agent turn.

Hub Debug → Session lists the durable ``/v2/session`` document. Inspector
and Analysis join the hops by ``req_id``. Those documents are written only
when the agent path posts the correlation headers, ``X-Zeus-Trace``,
``rewind=true``, and ``allow_pipeline``. ``run_data_verb`` rejects pipeline
and stamps a direct-read trace, so this harness does not use it.

Passwords stay in the process environment. ``password_env`` is the variable
name, never the secret.
"""

from __future__ import annotations

import copy
import os
from typing import Any

import provider_budget
import scope_brief


def chat_id_for(report_date: str, label: str, question_id: str) -> str:
    """Readable Hub chat id. Zeus mints the req id; this id is not a req id."""
    raw = f"ab-{report_date}-{label}-{question_id}"
    cleaned = []
    for char in raw:
        if char.isalnum() or char in {"-", "_"}:
            cleaned.append(char)
        else:
            cleaned.append("-")
    text = "".join(cleaned).strip("-")
    return text[:120] or "ab-turn"


def tool_rows_from_trace(steps: list, hops: list) -> list[dict]:
    """Tool steps plus the hop body, keyed by req_id.

    A posted ``return`` keeps its HTTP status. An empty summary stays local
    and is recorded as HTTP 0. A missing req_id on a real verb means Zeus
    did not echo ``X-Zeus-Req-Id``.
    """
    hops_by_req: dict[str, dict] = {}
    for hop in hops:
        if not isinstance(hop, dict):
            continue
        req_id = str(hop.get("req_id") or "")
        if req_id and req_id not in hops_by_req:
            hops_by_req[req_id] = hop
    rows: list[dict] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        kind = str(step.get("type") or "")
        if kind == "tool":
            req_id = str(step.get("req_id") or "")
            hop = hops_by_req.get(req_id) or {}
            body = hop.get("result_json")
            if not isinstance(body, dict):
                body = {}
            args = step.get("args") if isinstance(step.get("args"), dict) else {}
            status = step.get("status")
            if status is None:
                status = hop.get("status")
            rows.append(
                {
                    "round": step.get("round") or 0,
                    "verb": step.get("name") or "",
                    "args": args,
                    "http": status if status is not None else 0,
                    "req_id": req_id,
                    "body": body,
                }
            )
            continue
        if kind in {"return", "return_result"}:
            args = step.get("args") if isinstance(step.get("args"), dict) else {}
            status = step.get("status")
            http = status if isinstance(status, int) and status else 0
            req_id = str(step.get("req_id") or "")
            if http:
                body = {"posted": True}
            else:
                body = {"skipped": True, "reason": "terminal emit"}
            rows.append(
                {
                    "round": step.get("round") or 0,
                    "verb": "return",
                    "args": args,
                    "http": http,
                    "req_id": req_id,
                    "body": body,
                }
            )
    return rows


def _scope_login(bucket: str) -> tuple[str, str]:
    """Username plus the env var name that holds the password."""
    if bucket == "beer-sample":
        if os.environ.get("ZEUS_USER_BEER") and os.environ.get("ZEUS_PASS_BEER"):
            return os.environ["ZEUS_USER_BEER"], "ZEUS_PASS_BEER"
        return os.environ.get("ZEUS_USER", ""), "ZEUS_PASS"
    if bucket == "travel-sample":
        return os.environ.get("ZEUS_USER_TRAVEL", ""), "ZEUS_PASS_TRAVEL"
    return os.environ.get("ZEUS_USER", ""), "ZEUS_PASS"


def _load_symbols():
    src = scope_brief.client_src()
    if not (src / "zeus_client").is_dir():
        raise RuntimeError(
            f"zeus_client is not at {src}. Set ZEUS_CLIENT_SRC to the client's src directory."
        )
    entry = str(src)
    import sys

    if entry not in sys.path:
        sys.path.insert(0, entry)
    from zeus_client import ClientSettings, DataTarget, ZeusRuntime
    from zeus_client.adapters.llm_openai_compatible import OpenAICompatibleLlmClient
    from zeus_client.adapters.secrets_env.store import EnvSecretStore
    from zeus_client.adapters.zeus_http import HttpxZeusPort
    from zeus_client.adapters.zeus_http.catalog_remote import HttpxCatalogRemote
    from zeus_client.config.models import (
        DebugPolicy,
        LlmProviderConfig,
        RuntimeConfig,
        SemanticCacheConfig,
        ZeusEndpointConfig,
    )

    return {
        "ClientSettings": ClientSettings,
        "DataTarget": DataTarget,
        "ZeusRuntime": ZeusRuntime,
        "OpenAICompatibleLlmClient": OpenAICompatibleLlmClient,
        "EnvSecretStore": EnvSecretStore,
        "HttpxZeusPort": HttpxZeusPort,
        "HttpxCatalogRemote": HttpxCatalogRemote,
        "DebugPolicy": DebugPolicy,
        "LlmProviderConfig": LlmProviderConfig,
        "RuntimeConfig": RuntimeConfig,
        "SemanticCacheConfig": SemanticCacheConfig,
        "ZeusEndpointConfig": ZeusEndpointConfig,
    }


def open_runtime(
    *,
    zeus_url: str,
    provider: str,
    base_url: str,
    model: str,
    mode: str,
    max_rounds: int,
    budget: provider_budget.ProviderBudget | None = None,
):
    """One runtime. The harness opens one per scope so beer and travel can overlap.

    ``budget`` is one gate for every runtime in the process. Beer and travel
    share the provider key, so they share that gate. The wrapper sleeps.
    It does not shrink the prompt.

    The password is read later by env name. Session auth uses
    ``session_lifecycle.target``. ``ask`` sets that target to the question
    before each turn. The config target is beer only as a non-default
    placeholder. ``DataTarget()`` would be ``yelp-data``, which this harness
    must not mint.
    """
    sym = _load_symbols()
    beer_user, beer_env = _scope_login("beer-sample")
    travel_user, travel_env = _scope_login("travel-sample")
    endpoint = sym["ZeusEndpointConfig"](
        url=zeus_url.rstrip("/"),
        auth_mode="basic",
        username=None,
        password_env=None,
        timeout_s=90.0,
        scope_credentials={
            "beer-sample/_default": {"username": beer_user, "password_env": beer_env},
            "travel-sample/inventory": {"username": travel_user, "password_env": travel_env},
        },
    )
    # Product default ai_process_result=False stops after the first payload
    # (cheap_final). This harness keeps the tool loop open through max_rounds
    # so a find followed by a walk still runs. force_return_rounds_left=None
    # skips the client's early "call return now" nudge.
    settings = sym["ClientSettings"](
        ai_process_result=True,
        max_rounds=max_rounds,
        force_trace=True,
        mode=mode or "analytics",
        durable_sessions=True,
        force_return_rounds_left=None,
    )
    config = sym["RuntimeConfig"](
        profile="development",
        zeus=endpoint,
        target=sym["DataTarget"](bucket="beer-sample", scope="_default", collection="nodes"),
        llm=sym["LlmProviderConfig"](
            provider=provider,
            base_url=base_url,
            model=model,
            api_key_env="LLM_API_KEY",
            timeout_s=120.0,
        ),
        settings=settings,
        debug=sym["DebugPolicy"](rewind=True),
        semantic_cache=sym["SemanticCacheConfig"](enabled=False),
    )
    secrets = sym["EnvSecretStore"]()
    runtime = sym["ZeusRuntime"](config, secrets=secrets)
    runtime.services.zeus = sym["HttpxZeusPort"](
        endpoint=endpoint, secrets=secrets, journal=runtime.journal
    )
    llm = sym["OpenAICompatibleLlmClient"](
        config=config.llm, secrets=secrets, journal=runtime.journal
    )
    if budget is not None:
        llm = provider_budget.PacedLlm(llm, budget)
    runtime.services.llm = llm
    runtime.services.catalog_remote = sym["HttpxCatalogRemote"](
        endpoint=endpoint, secrets=secrets
    )
    # Init already built a session client. Rebuild is a no-op when one exists.
    # ask() still replaces session_lifecycle.target per question.
    runtime._ensure_session_lifecycle()
    runtime._symbols = sym
    return runtime


async def ask(
    runtime,
    *,
    pack: dict,
    question: dict,
    label: str,
    model: str,
    max_rounds: int,
    report_date: str,
    mode: str,
):
    """Run one question. The pack is copied so a beer brief cannot stick for travel."""
    sym = runtime._symbols
    bucket, scope = question["scope"].split("/", 1)
    target = sym["DataTarget"](
        bucket=bucket,
        scope=scope,
        collection=str(question.get("collection") or "nodes"),
    )
    life = runtime.services.session_lifecycle
    if life is None:
        runtime._ensure_session_lifecycle()
        life = runtime.services.session_lifecycle
    if life is not None:
        life.target = target
    # The round cap is on the cached basic login, not the Hub chat session.
    # Drop it so this question starts at bump 1. HTTP 400 stays in the score.
    port = getattr(getattr(runtime, "services", None), "zeus", None)
    forget = getattr(port, "forget_auth", None)
    if forget is not None:
        forget(target)
    settings = sym["ClientSettings"](
        ai_process_result=True,
        max_rounds=max_rounds,
        force_trace=True,
        mode=mode or "analytics",
        durable_sessions=True,
        force_return_rounds_left=None,
    )
    return await runtime.agent.run_turn(
        str(question.get("text") or ""),
        target=target,
        settings=settings,
        chat_request=copy.deepcopy(pack),
        chat_id=chat_id_for(report_date, label, str(question.get("id") or "q")),
        model=model,
        rewind=True,
    )


def _merged_system(result) -> str:
    """System text the turn sent. Empty when the live suffix is absent."""
    messages = getattr(result, "messages", None) or ()
    for message in messages:
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if isinstance(content, str) and "## SCOPE BRIEF" in content:
            return content
    return ""


def brief_flags(result) -> dict[str, Any]:
    """Report flags only. The brief text stays out of the evidence file.

    ``chars`` stays the UTF-8 byte length of the scope-brief slice plus the
    mini-schema slice. Walk paths are the next heading, so a turn that still
    has the merged system message also stores each section on its own.
    """
    debug = result.debug
    catalog = dict(debug.catalog or {})
    public = debug.public_trace if isinstance(debug.public_trace, dict) else {}
    inject = public.get("inject") if isinstance(public.get("inject"), dict) else {}
    slices = []
    chars = 0
    for key in ("scope_brief", "mini_schema"):
        section = inject.get(key) if isinstance(inject.get(key), dict) else {}
        text = section.get("text") if isinstance(section.get("text"), str) else ""
        if text:
            slices.append(text)
        try:
            chars += int(section.get("chars") or 0)
        except (TypeError, ValueError):
            chars += len(text.encode("utf-8"))
    scope = ""
    target = debug.target if isinstance(debug.target, dict) else {}
    bucket = str(target.get("bucket") or "")
    scope_name = str(target.get("scope") or "")
    if bucket and scope_name:
        scope = f"{bucket}/{scope_name}"
    flags: dict[str, Any] = {
        "scope": scope,
        "has_scope_brief": bool(catalog.get("has_scope_brief")),
        "has_mini_schema": bool(catalog.get("has_mini_schema")),
        "has_walk_paths": any("WALK_PATHS" in text for text in slices),
        "chars": chars,
        "client_version": str(debug.client_version or ""),
        "brief_sha12": catalog.get("brief_sha12") or "",
        "route": "/v1/ai/chat_request.json",
        "mode": "analytics",
    }
    suffix = scope_brief.injection_suffix(_merged_system(result))
    if not suffix:
        return flags
    counts = scope_brief.injection_counts(suffix)
    flags["has_walk_paths"] = counts["walk_paths"]["chars"] > 0
    flags["chars"] = counts["scope_brief"]["bytes"] + counts["mini_schema"]["bytes"]
    flags["injection_source"] = "turn"
    for name, piece in counts.items():
        flags[f"{name}_chars"] = piece["chars"]
        flags[f"{name}_bytes"] = piece["bytes"]
        flags[f"{name}_tk"] = piece["tk"]
        digest = str(piece.get("sha12") or "")
        if not digest:
            continue
        if name == "scope_brief":
            flags["brief_sha12"] = digest
        else:
            flags[f"{name}_sha12"] = digest
    return flags
