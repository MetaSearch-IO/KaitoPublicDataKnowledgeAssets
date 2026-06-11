#!/usr/bin/env python3
"""Validate every dataset JSON in this repository.

Run from the repository root (CI does):

    python3 scripts/validate_datasets.py

Exit code 0 = all datasets valid (warnings allowed), 1 = at least one error.

Rules are intentionally stricter for the new curation datasets
(crypto_companies, ai_companies) than for the legacy arena files, so that
existing automation (e.g. the Pre-TGE reverse-sync bot) keeps working
unchanged while new public contributions get tight feedback.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HANDLE_RE = re.compile(r"[A-Za-z0-9_]{1,15}")
SLUG_RE = re.compile(r"[a-z0-9_]{1,40}")
CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")

# An *active* category must keep at least this many member companies —
# new-category PRs must add the category and its members together.
MIN_CATEGORY_MEMBERS = 8

REPO_ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def _reject_dup_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate object key {key!r}")
        obj[key] = value
    return obj


def _reject_constant(name):
    raise ValueError(f"non-standard JSON constant {name!r}")


def load(rel_path: str):
    path = REPO_ROOT / rel_path
    if not path.exists():
        err(f"{rel_path}: file is missing")
        return None
    try:
        with path.open() as f:
            return json.load(
                f,
                object_pairs_hook=_reject_dup_keys,
                parse_constant=_reject_constant,
            )
    except (json.JSONDecodeError, ValueError) as exc:
        err(f"{rel_path}: invalid JSON — {exc}")
        return None


def req_str(
    rel_path: str,
    ident: str,
    obj: dict,
    field: str,
    *,
    strict: bool,
    allow_empty: bool = False,
) -> str | None:
    """Validate a required string field; returns the value when usable."""
    if field not in obj:
        err(f"{rel_path}: {ident}: '{field}' is required")
        return None
    value = obj[field]
    if not isinstance(value, str):
        err(f"{rel_path}: {ident}: '{field}' must be a string")
        return None
    if CONTROL_CHARS_RE.search(value):
        err(f"{rel_path}: {ident}: '{field}' contains control characters")
        return None
    if value != value.strip():
        msg = f"{rel_path}: {ident}: '{field}' has leading/trailing whitespace"
        err(msg) if strict else warn(msg)
        return value.strip() or None
    if not value:
        if allow_empty:
            return value
        err(f"{rel_path}: {ident}: '{field}' must not be empty")
        return None
    return value


def check_handle(rel_path: str, ident: str, handle, *, strict: bool) -> None:
    if handle is None:
        return
    if handle == "":
        warn(f"{rel_path}: {ident}: twitter_handle is empty — help us fill it in!")
        return
    if handle.startswith("@"):
        err(f"{rel_path}: {ident}: twitter_handle must not include the @ prefix")
        return
    if not HANDLE_RE.fullmatch(handle):
        msg = (
            f"{rel_path}: {ident}: twitter_handle {handle!r} is not a valid "
            "X/Twitter handle (1-15 chars, letters/digits/underscore)"
        )
        err(msg) if strict else warn(msg)


def check_no_at(rel_path: str, ident: str, field: str, value, *, strict: bool) -> None:
    if isinstance(value, str) and "@" in value:
        msg = f"{rel_path}: {ident}: '{field}' must not contain an @ mark"
        err(msg) if strict else warn(msg)


def check_ticker_list(rel_path: str, data, *, strict: bool, sorted_required: bool) -> None:
    """Shared shape for the ticker+remarks datasets."""
    if data is None:
        return
    if not isinstance(data, list):
        err(f"{rel_path}: top level must be a JSON array")
        return
    seen: dict[str, int] = {}
    keys_order: list[str] = []
    for i, entry in enumerate(data):
        ident = f"entry[{i}]"
        if not isinstance(entry, dict):
            err(f"{rel_path}: {ident} must be an object")
            continue
        ticker = req_str(rel_path, ident, entry, "ticker", strict=strict)
        if ticker is None:
            continue
        ident = ticker
        keys_order.append(ticker)
        if ticker in seen:
            err(f"{rel_path}: duplicate ticker {ticker!r} (entries {seen[ticker]} and {i})")
        seen.setdefault(ticker, i)
        remarks = entry.get("remarks")
        if not isinstance(remarks, dict):
            err(f"{rel_path}: {ident}: 'remarks' must be an object")
            continue
        display = req_str(rel_path, ident, remarks, "display_ticker", strict=strict)
        fullname = req_str(
            rel_path, ident, remarks, "fullname", strict=strict, allow_empty=True
        )
        handle = req_str(
            rel_path, ident, remarks, "twitter_handle", strict=strict, allow_empty=True
        )
        check_no_at(rel_path, ident, "display_ticker", display, strict=strict)
        check_no_at(rel_path, ident, "fullname", fullname, strict=strict)
        check_handle(rel_path, ident, handle, strict=strict)
    if sorted_required and keys_order != sorted(keys_order):
        first_bad = next(
            (k for k, s in zip(keys_order, sorted(keys_order)) if k != s), "?"
        )
        err(
            f"{rel_path}: entries must be sorted by ticker (ASCII ascending); "
            f"first out-of-order entry near {first_bad!r}"
        )


def check_ai_companies(rel_path: str, data, active_slugs: set[str]) -> None:
    if data is None:
        return
    if not isinstance(data, list):
        err(f"{rel_path}: top level must be a JSON array")
        return
    seen: dict[str, int] = {}
    keys_order: list[str] = []
    category_members: dict[str, int] = {slug: 0 for slug in active_slugs}
    for i, entry in enumerate(data):
        ident = f"entry[{i}]"
        if not isinstance(entry, dict):
            err(f"{rel_path}: {ident} must be an object")
            continue
        symbol = req_str(rel_path, ident, entry, "symbol", strict=True)
        if symbol is None:
            continue
        ident = symbol
        keys_order.append(symbol)
        if symbol in seen:
            err(f"{rel_path}: duplicate symbol {symbol!r} (entries {seen[symbol]} and {i})")
        seen.setdefault(symbol, i)
        remarks = entry.get("remarks")
        if not isinstance(remarks, dict):
            err(f"{rel_path}: {ident}: 'remarks' must be an object")
            continue
        display = req_str(rel_path, ident, remarks, "display_name", strict=True)
        fullname = req_str(
            rel_path, ident, remarks, "fullname", strict=True, allow_empty=True
        )
        handle = req_str(
            rel_path, ident, remarks, "twitter_handle", strict=True, allow_empty=True
        )
        check_no_at(rel_path, ident, "display_name", display, strict=True)
        check_no_at(rel_path, ident, "fullname", fullname, strict=True)
        check_handle(rel_path, ident, handle, strict=True)
        if "categories" not in remarks:
            err(f"{rel_path}: {ident}: remarks.categories is required")
            continue
        categories = remarks["categories"]
        if not isinstance(categories, list):
            err(f"{rel_path}: {ident}: remarks.categories must be an array")
            continue
        entry_seen: set[str] = set()
        for c in categories:
            if not isinstance(c, str):
                err(f"{rel_path}: {ident}: categories entries must be strings")
                continue
            if c in entry_seen:
                err(f"{rel_path}: {ident}: duplicate category {c!r}")
                continue
            entry_seen.add(c)
            if c not in active_slugs:
                err(
                    f"{rel_path}: {ident}: unknown category {c!r} — must be "
                    "an active slug from ai_companies/categories.json "
                    "(propose new categories in that file, in the same PR)"
                )
            else:
                category_members[c] += 1
    if keys_order != sorted(keys_order):
        first_bad = next(
            (k for k, s in zip(keys_order, sorted(keys_order)) if k != s), "?"
        )
        err(
            f"{rel_path}: entries must be sorted by symbol (ASCII ascending); "
            f"first out-of-order entry near {first_bad!r}"
        )
    for slug, count in sorted(category_members.items()):
        if count < MIN_CATEGORY_MEMBERS:
            err(
                f"ai_companies/categories.json: active category {slug!r} has only "
                f"{count} member compan{'y' if count == 1 else 'ies'} in {rel_path} "
                f"— active categories need at least {MIN_CATEGORY_MEMBERS} "
                "(add members in the same PR, or mark the category 'retired')"
            )


def check_categories(rel_path: str, data) -> set[str]:
    active: set[str] = set()
    if data is None:
        return active
    if not isinstance(data, list):
        err(f"{rel_path}: top level must be a JSON array")
        return active
    seen: set[str] = set()
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            err(f"{rel_path}: entry[{i}] must be an object")
            continue
        slug = entry.get("slug")
        if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            err(
                f"{rel_path}: entry[{i}]: 'slug' must be 1-40 chars of "
                "lowercase letters/digits/underscore"
            )
            continue
        if slug in seen:
            err(f"{rel_path}: duplicate slug {slug!r}")
        seen.add(slug)
        if req_str(rel_path, slug, entry, "display_name", strict=True) is None:
            continue
        status = entry.get("status")
        if status not in ("active", "retired"):
            err(f"{rel_path}: {slug}: 'status' must be 'active' or 'retired'")
        elif status == "active":
            active.add(slug)
    return active


def check_vc(affil_path: str, firms_path: str) -> None:
    affiliations = load(affil_path)
    firms = load(firms_path)
    if affiliations is None or firms is None:
        return
    if not isinstance(affiliations, list) or not isinstance(firms, list):
        err("vc datasets must be JSON arrays")
        return
    firm_ids = {
        f.get("twitter_user_id")
        for f in firms
        if isinstance(f, dict) and f.get("twitter_user_id")
    }
    for i, entry in enumerate(affiliations):
        if not isinstance(entry, dict):
            err(f"{affil_path}: entry[{i}] must be an object")
            continue
        user_id = entry.get("twitter_user_id")
        if not isinstance(user_id, str) or not user_id.strip():
            err(f"{affil_path}: entry[{i}]: 'twitter_user_id' must be a non-empty string")
        for firm_id in entry.get("vc_affiliations") or []:
            if firm_id not in firm_ids:
                warn(
                    f"{affil_path}: {user_id or i}: affiliated firm {firm_id!r} has "
                    f"no entry in {firms_path}"
                )


def main() -> int:
    # New curation datasets — strict.
    active_slugs = check_categories(
        "ai_companies/categories.json", load("ai_companies/categories.json")
    )
    check_ticker_list(
        "crypto_companies/crypto_companies.json",
        load("crypto_companies/crypto_companies.json"),
        strict=True,
        sorted_required=True,
    )
    check_ai_companies(
        "ai_companies/ai_companies.json",
        load("ai_companies/ai_companies.json"),
        active_slugs,
    )

    # Legacy arena datasets — keep existing automation green.
    for rel in (
        "Exchange_Arena/Exchange_Arena.json",
        "PreTGE_Project/PreTGE_Project.json",
        "information_markets/information_markets_projects.json",
    ):
        check_ticker_list(rel, load(rel), strict=False, sorted_required=False)

    check_vc("vc/vc_twitter_affiliations.json", "vc/vc_firms.json")

    # Anything else with a .json extension must at least parse.
    checked = {
        "ai_companies/categories.json",
        "ai_companies/ai_companies.json",
        "crypto_companies/crypto_companies.json",
        "Exchange_Arena/Exchange_Arena.json",
        "PreTGE_Project/PreTGE_Project.json",
        "information_markets/information_markets_projects.json",
        "vc/vc_twitter_affiliations.json",
        "vc/vc_firms.json",
    }
    for path in sorted(REPO_ROOT.rglob("*.json")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(".") or rel in checked:
            continue
        load(rel)

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(
        f"\nvalidate_datasets: {len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
