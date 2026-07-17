#!/usr/bin/env python3
"""Generate a BMSTable-compatible FORCE RATE chart-constant table."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from pathlib import Path


FALLBACK_METADATA: dict[str, dict[str, object]] = {
    "ff2d2ffa4ae22da44b8cc3f20597a899": {
        "title": "Dandelion Sparkle!! -ふわふわ-",
        "artist": "p_d/s_h / Artwork : ふりっと★",
        "body_url": "https://lr2ir.com/charts/ff2d2ffa4ae22da44b8cc3f20597a899",
        "diff_url": "",
    },
    "ff82e0003d07d1933f7a12c87c84218f": {
        "title": "失望Choco (・ω・)",
        "artist": "LeaF/さ",
        "body_url": "https://lr2ir.com/charts/ff82e0003d07d1933f7a12c87c84218f",
        "diff_url": "",
    },
    "fff439eaf47b9c8a9d2cd00f128ca902": {
        "title": "Aqua Regia Squall [F]",
        "artist": "DJ owl-light vs xi / obj:Fender",
        "body_url": "https://lr2ir.com/charts/fff439eaf47b9c8a9d2cd00f128ca902",
        "diff_url": "",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--constants", required=True, type=Path)
    parser.add_argument("--archive-db", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = json.loads(args.constants.read_text(encoding="utf-8"))
    charts = source.get("charts", [])
    md5s = [str(chart.get("md5", "")).lower() for chart in charts]

    database_uri = f"file:{args.archive_db.resolve().as_posix()}?mode=ro"
    metadata: dict[str, dict[str, object]] = {}
    with sqlite3.connect(database_uri, uri=True) as connection:
        connection.row_factory = sqlite3.Row
        for offset in range(0, len(md5s), 500):
            chunk = md5s[offset : offset + 500]
            placeholders = ",".join("?" for _ in chunk)
            query = (
                "SELECT md5, title, artist, body_url, diff_url "
                f"FROM chart WHERE md5 IN ({placeholders})"
            )
            for row in connection.execute(query, chunk):
                metadata[row["md5"].lower()] = dict(row)

    rows: list[dict[str, object]] = []
    missing: list[str] = []
    for chart in charts:
        md5 = str(chart.get("md5", "")).lower()
        info = metadata.get(md5) or FALLBACK_METADATA.get(md5)
        if info is None:
            missing.append(md5)
            continue

        constant = min(27.0, max(1.0, float(chart["chartConstant"])))
        level = min(27, max(1, math.floor(constant)))
        rows.append(
            {
                "level": str(level),
                "title": info["title"],
                "artist": info["artist"] or "不明",
                "md5": md5,
                "url": info["body_url"] or "",
                "url_diff": info["diff_url"] or "",
                "constant": f"{constant:.2f}",
                "source_table": chart.get("sourceTable", ""),
                "source_level": chart.get("difficulty", ""),
            }
        )

    rows.sort(
        key=lambda row: (
            int(str(row["level"])),
            float(str(row["constant"])),
            str(row["title"]),
        )
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated {len(rows)} charts: {args.output}")
    if missing:
        print(f"Warning: metadata unavailable for {len(missing)} charts")
        for md5 in missing:
            print(f"  {md5}")


if __name__ == "__main__":
    main()
