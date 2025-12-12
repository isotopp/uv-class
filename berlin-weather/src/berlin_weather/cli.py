from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date
from typing import Any

import httpx


BRIGHTSKY_WEATHER_URL = "https://api.brightsky.dev/weather"


@dataclass(frozen=True)
class WeatherNow:
    time: str
    temperature_c: float | None
    precipitation_mm: float | None
    wind_speed_ms: float | None


def _pick_latest_weather(payload: dict[str, Any]) -> WeatherNow:
    weather = payload.get("weather")
    if not isinstance(weather, list) or not weather:
        raise ValueError("Bright Sky returned no weather records for this date.")

    last = weather[-1]
    if not isinstance(last, dict):
        raise ValueError("Bright Sky payload format was unexpected.")

    return WeatherNow(
        time=str(last.get("timestamp", "")),
        temperature_c=(last.get("temperature") if isinstance(last.get("temperature"), (int, float)) else None),
        precipitation_mm=(last.get("precipitation") if isinstance(last.get("precipitation"), (int, float)) else None),
        wind_speed_ms=(last.get("wind_speed") if isinstance(last.get("wind_speed"), (int, float)) else None),
    )


def fetch_weather_for(
        *,
        lat: float,
        lon: float,
        day: date,
        client: httpx.Client,
) -> WeatherNow:
    params = {
        "lat": f"{lat:.5f}",
        "lon": f"{lon:.5f}",
        "date": day.isoformat(),
    }

    r = client.get(BRIGHTSKY_WEATHER_URL, params=params)
    r.raise_for_status()
    payload = r.json()
    if not isinstance(payload, dict):
        raise ValueError("Bright Sky payload was not a JSON object.")
    return _pick_latest_weather(payload)


def main() -> int:
    berlin_lat = 52.52000
    berlin_lon = 13.40500
    today = date.today()

    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {
        "User-Agent": "berlin-weather-training/1.0",
        "Accept": "application/json",
    }

    try:
        with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
            w = fetch_weather_for(lat=berlin_lat, lon=berlin_lon, day=today, client=client)

        print(f"Bright Sky - Berlin - {today.isoformat()}")
        print(f"time: {w.time}")
        print(f"temperature: {w.temperature_c} C")
        print(f"precipitation: {w.precipitation_mm} mm")
        print(f"wind speed: {w.wind_speed_ms} m/s")
        return 0

    except httpx.HTTPError as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
