#!/usr/bin/env python3
"""Fetch chess.com stats for a single user and write to assets/data/chess_stats.json.

Rapid time control only. Runs serially because chess.com rate-limits parallel
requests with HTTP 429 even from the same IP.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib import request, error

USERNAME = "nu11pointer"
BASE = f"https://api.chess.com/pub/player/{USERNAME}"
HEADERS = {
    # chess.com requires a descriptive UA; anonymous requests get 403.
    "User-Agent": "Abrar-Abir.github.io stats fetcher (contact: abir@cmu.edu)",
    "Accept": "application/json",
}
OUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "data" / "chess_stats.json"


def get_json(url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            req = request.Request(url, headers=HEADERS)
            with request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as e:
            if e.code == 404:
                return None
            print(f"HTTP {e.code} on {url} (attempt {attempt + 1})", file=sys.stderr)
        except Exception as e:
            print(f"error on {url}: {e} (attempt {attempt + 1})", file=sys.stderr)
        time.sleep(2 ** attempt)
    return None


def archive_rapid_summary(archive_url: str) -> tuple[int | None, set[str]]:
    """Return (end-of-month rapid rating, set of UTC date strings with a rapid game)."""
    data = get_json(archive_url)
    if not data:
        return None, set()
    games = data.get("games", [])
    rapid_dates: set[str] = set()
    last_rating: int | None = None
    for g in games:
        if g.get("time_class") != "rapid":
            continue
        end_time = g.get("end_time")
        if end_time:
            day = datetime.fromtimestamp(end_time, tz=timezone.utc).strftime("%Y-%m-%d")
            rapid_dates.add(day)
        white = g.get("white", {})
        black = g.get("black", {})
        if white.get("username", "").lower() == USERNAME.lower():
            last_rating = white.get("rating")
        elif black.get("username", "").lower() == USERNAME.lower():
            last_rating = black.get("rating")
    return last_rating, rapid_dates


def compute_streak(dates: set[str]) -> int:
    """Consecutive UTC days with a rapid game, ending today or yesterday."""
    if not dates:
        return 0
    today = datetime.now(timezone.utc).date()
    cursor = today if today.strftime("%Y-%m-%d") in dates else today - timedelta(days=1)
    streak = 0
    while cursor.strftime("%Y-%m-%d") in dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def main() -> int:
    profile = get_json(BASE) or {}
    stats = get_json(f"{BASE}/stats") or {}
    archives = (get_json(f"{BASE}/games/archives") or {}).get("archives", [])

    country_url = profile.get("country") or ""
    country_code = country_url.rstrip("/").split("/")[-1] if country_url else None

    rapid_history: list[dict] = []
    all_rapid_dates: set[str] = set()
    for url in archives:
        # archive URLs end in /YYYY/MM
        parts = url.rstrip("/").split("/")
        month_label = f"{parts[-2]}-{parts[-1]}"
        rating, dates = archive_rapid_summary(url)
        all_rapid_dates |= dates
        if rating is not None:
            rapid_history.append({"month": month_label, "rating": rating})
        time.sleep(0.5)  # be polite

    streak_days = compute_streak(all_rapid_dates)

    out = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile": {
            "username": profile.get("username"),
            "title": profile.get("title"),
            "country": profile.get("country"),  # URL to country resource
            "country_code": country_code,
            "joined": profile.get("joined"),  # unix ts
            "followers": profile.get("followers"),
            "avatar": profile.get("avatar"),
            "url": profile.get("url"),
        },
        "stats": {
            "chess_rapid": stats.get("chess_rapid"),
            "rapid_streak_days": streak_days,
        },
        "rating_history": {
            "rapid": rapid_history,
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
