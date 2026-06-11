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

HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
SLUG_RE = re.compile(r"^[a-z0-9_]{1,40}$")

REPO_ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load(rel_path: str):
    path = REPO_ROOT / rel_path
    if not path.exists():
        err(f"{rel_path}: file is missing")
        return None
    try:
        with path.open() as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        err(f"{rel_path}: invalid JSON — {exc}")
        return None


def check_handle(rel_path: str, ident: str, handle, *, strict: bool) -> None:
    if not isinstance(handle, str):
        err(f"{rel_path}: {ident}: twitter_handle must be a string")
        return
    if handle == "":
        warn(f"{rel_path}: {ident}: twitter_handle is empty — help us fill it in!")
        return
    if handle.startswith("@"):
        err(f"{rel_path}: {ident}: twitter_handle must not include the @ prefix")
        return
    if not HANDLE_RE.match(handle):
        msg = (
            f"{rel_path}: {ident}: twitter_handle {handle!r} is not a valid "
            "X/Twitter handle (1-15 chars, letters/digits/underscore)"
        )
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
        ticker = entry.get("ticker")
        if not isinstance(ticker, str) or not ticker.strip():
            err(f"{rel_path}: {ident}: 'ticker' must be a non-empty string")
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
        for field in ("display_ticker", "fullname", "twitter_handle"):
            if field not in remarks:
                err(f"{rel_path}: {ident}: remarks.{field} is required")
        if isinstance(remarks.get("display_ticker"), str) and not remarks["display_ticker"].strip():
            err(f"{rel_path}: {ident}: remarks.display_ticker must not be empty")
        if "twitter_handle" in remarks:
            check_handle(rel_path, ident, remarks["twitter_handle"], strict=strict)
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
    for i, entry in enumerate(data):
        ident = f"entry[{i}]"
        if not isinstance(entry, dict):
            err(f"{rel_path}: {ident} must be an object")
            continue
        symbol = entry.get("symbol")
        if not isinstance(symbol, str) or not symbol.strip():
            err(f"{rel_path}: {ident}: 'symbol' must be a non-empty string")
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
        for field in ("display_name", "fullname", "twitter_handle", "categories"):
            if field not in remarks:
                err(f"{rel_path}: {ident}: remarks.{field} is required")
        if isinstance(remarks.get("display_name"), str) and not remarks["display_name"].strip():
            err(f"{rel_path}: {ident}: remarks.display_name must not be empty")
        if "twitter_handle" in remarks:
            check_handle(rel_path, ident, remarks["twitter_handle"], strict=True)
        categories = remarks.get("categories")
        if categories is not None:
            if not isinstance(categories, list):
                err(f"{rel_path}: {ident}: remarks.categories must be an array")
            else:
                for c in categories:
                    if c not in active_slugs:
                        err(
                            f"{rel_path}: {ident}: unknown category {c!r} — must be "
                            "an active slug from ai_companies/categories.json "
                            "(propose new categories in that file, in the same PR)"
                        )
    if keys_order != sorted(keys_order):
        first_bad = next(
            (k for k, s in zip(keys_order, sorted(keys_order)) if k != s), "?"
        )
        err(
            f"{rel_path}: entries must be sorted by symbol (ASCII ascending); "
            f"first out-of-order entry near {first_bad!r}"
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
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            err(f"{rel_path}: entry[{i}]: 'slug' must match {SLUG_RE.pattern}")
            continue
        if slug in seen:
            err(f"{rel_path}: duplicate slug {slug!r}")
        seen.add(slug)
        if not isinstance(entry.get("display_name"), str) or not entry["display_name"].strip():
            err(f"{rel_path}: {slug}: 'display_name' must be a non-empty string")
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
