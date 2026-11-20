#!/usr/bin/env python3
"""Compute monthly climate normals per place and write normals.json.

Normals change slowly, so this is not part of the hourly workflow: run it by
hand when the place list changes or once a year.

Source: Open-Meteo archive API, daily values for PERIOD, aggregated per month.
Places are batched: one request per BATCH places, spaced out, because the
archive endpoint enforces a per-minute request limit.
Stdlib only.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

UA = "weather-hub/1.0 (+https://github.com/Rulac/weather-hub)"

PLACES = [
    {"id": "zagreb", "name": "Zagreb", "lat": 45.8150, "lon": 15.9819, "ele": 120},
    {"id": "sljeme", "name": "Sljeme", "lat": 45.9097, "lon": 15.9436, "ele": 1035},
    {"id": "komiza", "name": "Komiža", "lat": 43.0447, "lon": 16.0919, "ele": 20},
    {"id": "krk", "name": "Krk", "lat": 45.0258, "lon": 14.5753, "ele": 20},
    {"id": "samobor", "name": "Samobor", "lat": 45.8031, "lon": 15.7119, "ele": 160},
    {"id": "motovun", "name": "Motovun", "lat": 45.3361, "lon": 13.8286, "ele": 270},
    {"id": "losinj", "name": "Mali Lošinj", "lat": 44.5311, "lon": 14.4700, "ele": 10},
]

PERIOD_START = 2020
PERIOD_END = 2024
BATCH = 3
PAUSE = 25
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "normals.json")


def get_json(url, tries=5):
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                print("  429, waiting 65s")
                time.sleep(65)
            else:
                time.sleep(5 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(5 * (attempt + 1))
    raise last


def monthly_stats(block):
    daily = block.get("daily") or {}
    times = daily.get("time") or []
    buckets = {}
    for i, iso in enumerate(times):
        bucket = buckets.setdefault(int(iso[5:7]),
                                    {"max": [], "min": [], "mean": [], "precip": []})
        for field, key in (("temperature_2m_max", "max"), ("temperature_2m_min", "min"),
                           ("temperature_2m_mean", "mean"), ("precipitation_sum", "precip")):
            series = daily.get(field) or []
            value = series[i] if i < len(series) else None
            if value is not None:
                bucket[key].append(value)

    out = {"tmax": [], "tmin": [], "tmean": [], "precip": []}
    for month in range(1, 13):
        bucket = buckets.get(month, {})
        for key, name, digits in (("max", "tmax", 1), ("min", "tmin", 1),
                                  ("mean", "tmean", 1)):
            values = bucket.get(key) or []
            out[name].append(round(sum(values) / len(values), digits) if values else None)
        precip = bucket.get("precip") or []
        out["precip"].append(round(sum(precip) / max(1, PERIOD_END - PERIOD_START + 1))
                             if precip else None)
    return out


def fetch_batch(batch):
    q = urllib.parse.urlencode({
        "latitude": ",".join("%.4f" % p["lat"] for p in batch),
        "longitude": ",".join("%.4f" % p["lon"] for p in batch),
        "elevation": ",".join("%d" % p["ele"] for p in batch),
        "start_date": "%d-01-01" % PERIOD_START,
        "end_date": "%d-12-31" % PERIOD_END,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Zagreb",
    })
    data = get_json("https://archive-api.open-meteo.com/v1/archive?" + q)
    if isinstance(data, dict):
        data = [data]
    return data


def main():
    places = {}
    failed = []
    for start in range(0, len(PLACES), BATCH):
        batch = PLACES[start:start + BATCH]
        try:
            blocks = fetch_batch(batch)
        except Exception as e:
            failed.extend("%s: %s" % (p["id"], e) for p in batch)
            print("batch %d-%d FAILED: %s" % (start, start + len(batch), e))
            continue
        for place, block in zip(batch, blocks):
            places[place["id"]] = monthly_stats(block)
            print("  %-16s ok" % place["name"])
        time.sleep(PAUSE)

    payload = {
        "period": "%d-%d" % (PERIOD_START, PERIOD_END),
        "generated": date.today().isoformat(),
        "places": places,
        "errors": failed,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote %s: %d places, %d failures" % (OUT, len(places), len(failed)))
    return 0 if places else 1


if __name__ == "__main__":
    sys.exit(main())
