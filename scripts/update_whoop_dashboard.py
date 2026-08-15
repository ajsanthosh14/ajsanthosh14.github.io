#!/usr/bin/env python3
import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

WHOOP_WORKOUTS_URL = "https://api.prod.whoop.com/developer/v2/activity/workout"
LOCAL_TZ = ZoneInfo("America/Denver")
OUT_PATH = Path("assets/data/whoop-week.json")


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def friendly_sport(name: str) -> str:
    special = {
        "muay-thai": "Muay Thai",
        "martial-arts": "Martial Arts",
        "weightlifting": "Weightlifting",
        "activity": "Activity",
    }
    return special.get(name, name.replace("-", " ").title())


def format_duration(seconds: float) -> str:
    total_minutes = int(round(seconds / 60.0))
    hours, minutes = divmod(total_minutes, 60)
    if hours and minutes:
        return f"{hours}h {minutes}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"


def fetch_json(url: str, access_token: str) -> dict:
    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "SanthoshPortfolio-WHOOP/1.0",
        },
    )
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def fetch_week_workouts(access_token: str, start_utc: datetime, end_utc: datetime) -> list[dict]:
    records: list[dict] = []
    next_token = None
    while True:
        params = {
            "limit": 25,
            "start": start_utc.isoformat().replace("+00:00", "Z"),
            "end": end_utc.isoformat().replace("+00:00", "Z"),
        }
        if next_token:
            params["nextToken"] = next_token
        payload = fetch_json(f"{WHOOP_WORKOUTS_URL}?{urlencode(params)}", access_token)
        records.extend(payload.get("records", []))
        next_token = payload.get("next_token")
        if not next_token:
            break
    return records


def main() -> None:
    access_token = os.environ.get("WHOOP_ACCESS_TOKEN")
    if not access_token:
        raise SystemExit("WHOOP_ACCESS_TOKEN is required")

    now_local = datetime.now(LOCAL_TZ)
    week_start_local = (now_local - timedelta(days=now_local.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_utc = week_start_local.astimezone(timezone.utc)
    end_utc = now_local.astimezone(timezone.utc)

    raw_records = fetch_week_workouts(access_token, start_utc, end_utc)

    workouts = []
    for record in raw_records:
        try:
            start = parse_dt(record["start"])
            end = parse_dt(record["end"])
        except (KeyError, TypeError, ValueError):
            continue
        local_start = start.astimezone(LOCAL_TZ)
        if local_start < week_start_local or local_start > now_local:
            continue
        workouts.append((record, start, end))

    total_seconds = sum(max(0.0, (end - start).total_seconds()) for _, start, end in workouts)
    strains = []
    peak_hrs = []
    sports = Counter()

    for record, _, _ in workouts:
        sports[friendly_sport(record.get("sport_name", "activity"))] += 1
        score = record.get("score") or {}
        strain = score.get("strain")
        max_hr = score.get("max_heart_rate")
        if isinstance(strain, (int, float)):
            strains.append(float(strain))
        if isinstance(max_hr, (int, float)):
            peak_hrs.append(int(max_hr))

    activities = [
        {"sport": sport, "count": count}
        for sport, count in sorted(sports.items(), key=lambda item: (-item[1], item[0]))
    ]

    core = {
        "source": "WHOOP",
        "timezone": "America/Denver",
        "week_start": week_start_local.date().isoformat(),
        "workouts": len(workouts),
        "training_seconds": round(total_seconds),
        "training_time": format_duration(total_seconds),
        "average_strain": round(sum(strains) / len(strains), 1) if strains else None,
        "peak_hr": max(peak_hrs) if peak_hrs else None,
        "activities": activities,
    }

    previous = None
    if OUT_PATH.exists():
        try:
            previous = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    comparable_previous = None
    if isinstance(previous, dict):
        comparable_previous = {k: previous.get(k) for k in core}

    if comparable_previous == core:
        print("WHOOP dashboard data unchanged; keeping existing file.")
        return

    data = {
        **core,
        "updated_at": end_utc.isoformat().replace("+00:00", "Z"),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        f"WHOOP dashboard: {data['workouts']} workouts, {data['training_time']}, "
        f"avg strain {data['average_strain']}, peak HR {data['peak_hr']}"
    )


if __name__ == "__main__":
    main()
