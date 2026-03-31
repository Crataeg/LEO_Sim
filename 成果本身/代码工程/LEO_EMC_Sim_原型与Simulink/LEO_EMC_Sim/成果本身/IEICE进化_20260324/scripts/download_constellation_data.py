# -*- coding: utf-8 -*-
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "downloads" / "constellation_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

SOURCES = [
    {
        "name": "starlink_json",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=json-pretty",
        "filename": "celestrak_starlink_gp.json",
        "description": "Current GP data for Starlink in JSON format.",
    },
    {
        "name": "starlink_2le",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=2le",
        "filename": "celestrak_starlink_gp.2le",
        "description": "Current GP data for Starlink in TLE format.",
    },
    {
        "name": "oneweb_json",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=json-pretty",
        "filename": "celestrak_oneweb_gp.json",
        "description": "Current GP data for OneWeb in JSON format.",
    },
    {
        "name": "oneweb_2le",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=2le",
        "filename": "celestrak_oneweb_gp.2le",
        "description": "Current GP data for OneWeb in TLE format.",
    },
    {
        "name": "qianfan_json",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=qianfan&FORMAT=json-pretty",
        "filename": "celestrak_qianfan_gp.json",
        "description": "Current GP data for Qianfan in JSON format.",
    },
    {
        "name": "qianfan_2le",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=qianfan&FORMAT=2le",
        "filename": "celestrak_qianfan_gp.2le",
        "description": "Current GP data for Qianfan in TLE format.",
    },
    {
        "name": "active_csv",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=csv",
        "filename": "celestrak_active_gp.csv",
        "description": "Current GP data for all active satellites in CSV format.",
    },
    {
        "name": "celestrak_group_index",
        "url": "https://celestrak.org/NORAD/elements/index.php?FORMAT=csv",
        "filename": "celestrak_group_index.html",
        "description": "CelesTrak group index page used to expand to more constellations later.",
    },
]


def fetch(url: str) -> Tuple[bytes, str]:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read(), resp.getheader("Content-Type") or ""


def main() -> None:
    rows = []
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    for item in SOURCES:
        payload, content_type = fetch(item["url"])
        out = DATA_DIR / item["filename"]
        out.write_bytes(payload)
        rows.append(
            {
                "name": item["name"],
                "description": item["description"],
                "url": item["url"],
                "content_type": content_type,
                "saved_path": str(out),
                "size_bytes": len(payload),
                "fetched_at_utc": fetched_at,
            }
        )

    manifest_csv = DATA_DIR / "constellation_download_manifest.csv"
    with manifest_csv.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "description",
                "url",
                "content_type",
                "saved_path",
                "size_bytes",
                "fetched_at_utc",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    geesat_rows = []
    with (DATA_DIR / "celestrak_active_gp.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            upper_name = row["OBJECT_NAME"].upper()
            if "GEESAT" in upper_name or "GEELY" in upper_name:
                geesat_rows.append(row)

    geesat_csv = DATA_DIR / "celestrak_geesat_subset.csv"
    if geesat_rows:
        with geesat_csv.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(geesat_rows[0].keys()))
            writer.writeheader()
            writer.writerows(geesat_rows)

    quick_stats = {
        "fetched_at_utc": fetched_at,
        "starlink_count": len(json.loads((DATA_DIR / "celestrak_starlink_gp.json").read_text(encoding="utf-8"))),
        "oneweb_count": len(json.loads((DATA_DIR / "celestrak_oneweb_gp.json").read_text(encoding="utf-8"))),
        "qianfan_count": len(json.loads((DATA_DIR / "celestrak_qianfan_gp.json").read_text(encoding="utf-8"))),
        "geesat_count": len(geesat_rows),
    }
    (DATA_DIR / "constellation_quick_stats.json").write_text(
        json.dumps(quick_stats, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(quick_stats, ensure_ascii=False))
    print(manifest_csv)


if __name__ == "__main__":
    main()
