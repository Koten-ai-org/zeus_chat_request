"""Load the live scope brief through kotenai-zeus-client.

Zeus returns one chat_request per scope. The suffix that starts at
``## SCOPE BRIEF`` includes ``## MINI-SCHEMA`` and ``## WALK_PATHS``.
The local pack keeps its own system text and verbs. This module splices
that live suffix on, using the client's catalog fetch and merge.

The sibling checkout is ``../zeus_client_python``. Override it with
``ZEUS_CLIENT_SRC`` pointing at that repo's ``src`` directory. The
interpreter needs ``httpx``, which the client virtualenv already has.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import sys
from pathlib import Path


def client_src() -> Path:
    override = os.environ.get("ZEUS_CLIENT_SRC", "").strip()
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[2] / "zeus_client_python" / "src"


def _import_client():
    src = client_src()
    if not (src / "zeus_client").is_dir():
        raise RuntimeError(
            f"zeus_client is not at {src}. Set ZEUS_CLIENT_SRC to the client's src directory."
        )
    entry = str(src)
    if entry not in sys.path:
        sys.path.insert(0, entry)
    try:
        from zeus_client._version import __version__
        from zeus_client.adapters.zeus_http.catalog_remote import HttpxCatalogRemote
        from zeus_client.config.models import ZeusEndpointConfig
        from zeus_client.domain.catalog import extract_scope_brief, merge_scope_brief
    except ImportError as exc:
        raise RuntimeError(
            "Could not import zeus_client. Run this harness with the client virtualenv, "
            "which provides httpx: "
            "../zeus_client_python/.venv/bin/python"
        ) from exc
    return {
        "version": __version__,
        "HttpxCatalogRemote": HttpxCatalogRemote,
        "ZeusEndpointConfig": ZeusEndpointConfig,
        "extract_scope_brief": extract_scope_brief,
        "merge_scope_brief": merge_scope_brief,
    }


async def _fetch(base_url: str, bucket: str, scope: str, mode: str, session: str) -> dict:
    client = _import_client()
    remote = client["HttpxCatalogRemote"](client["ZeusEndpointConfig"](url=base_url))
    headers = {"X-Zeus-Session": session} if session else {}
    try:
        body = await remote.fetch_chat_request(bucket, scope, mode, headers=headers)
    finally:
        await remote.aclose()
    brief = client["extract_scope_brief"](body if isinstance(body, dict) else {})
    return {
        "text": brief,
        "has_scope_brief": "## SCOPE BRIEF" in brief,
        "has_mini_schema": "## MINI-SCHEMA" in brief,
        "has_walk_paths": "## WALK_PATHS" in brief,
        "chars": len(brief),
        "client_version": client["version"],
        "route": "/v1/ai/chat_request.json",
        "scope": f"{bucket}/{scope}",
        "mode": mode,
    }


def live_scope_brief(base_url: str, bucket: str, scope: str, mode: str, session: str) -> dict:
    """Fetch and describe the live brief. Raises when the client or Zeus call fails."""
    return asyncio.run(_fetch(base_url, bucket, scope, mode, session))


def _markdown_section(text: str, heading_prefix: str) -> str:
    """``## HEADING`` through the next top-level ``## ``. ``###`` stays inside.

    Same cut as ``zeus_client.application.detective.extract.slice_block``.
    """
    if not text or not heading_prefix:
        return ""
    idx = text.find(heading_prefix)
    if idx < 0:
        return ""
    lines = text[idx:].split("\n")
    kept = [lines[0]]
    for line in lines[1:]:
        if line.startswith("## ") and not line.startswith(heading_prefix):
            break
        kept.append(line)
    return "\n".join(kept).rstrip("\n")


def injection_suffix(text: str) -> str:
    """Text from ``## SCOPE BRIEF`` through the end of the system message."""
    marker = "## SCOPE BRIEF"
    idx = (text or "").find(marker)
    if idx < 0:
        return ""
    return text[idx:].strip()


def _injection_piece(text: str) -> dict[str, int | str]:
    raw = (text or "").encode("utf-8")
    nbytes = len(raw)
    tokens = 0 if nbytes <= 0 else max(1, (nbytes + 3) // 4)
    digest = hashlib.sha256(raw).hexdigest()[:12] if text else ""
    return {"chars": len(text or ""), "bytes": nbytes, "tk": tokens, "sha12": digest}


def injection_counts(text: str) -> dict[str, dict[str, int | str]]:
    """Scope brief, mini-schema, walk paths, and the full suffix. No brief text.

    The scope-brief slice stops at ``## MINI-SCHEMA``. The mini-schema slice
    stops at the next ``## `` heading, which is where ``## WALK_PATHS`` starts.
    ``full`` is the suffix the client appends.
    """
    suffix = injection_suffix(text)
    brief = _markdown_section(suffix, "## SCOPE BRIEF")
    mini_at = brief.find("## MINI-SCHEMA")
    if mini_at > 0:
        brief = brief[:mini_at].rstrip("\n")
    brief = brief.strip()
    mini = _markdown_section(suffix, "## MINI-SCHEMA").strip()
    walk = _markdown_section(suffix, "## WALK_PATHS").strip()
    return {
        "scope_brief": _injection_piece(brief),
        "mini_schema": _injection_piece(mini),
        "walk_paths": _injection_piece(walk),
        "full": _injection_piece(suffix),
    }


def merge_pack(pack: dict, brief: str) -> dict:
    """Return a copy of the pack with the live brief appended to its system text."""
    client = _import_client()
    if not brief:
        return pack
    return client["merge_scope_brief"](pack, brief)
