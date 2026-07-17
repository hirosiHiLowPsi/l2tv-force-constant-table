#!/usr/bin/env python3
"""Validate generated FORCE RATE BMSTable data without Node dependencies."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "force-constant-table.json"


def main() -> None:
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert isinstance(rows, list), "data must be a JSON array"
    assert len(rows) == 1265, f"unexpected chart count: {len(rows)}"

    md5s: set[str] = set()
    counts: Counter[str] = Counter()
    for row in rows:
        md5 = row["md5"]
        assert isinstance(md5, str) and len(md5) == 32
        assert md5 not in md5s, f"duplicate MD5: {md5}"
        md5s.add(md5)

        constant = float(row["constant"])
        assert 1.0 <= constant <= 27.0
        expected_level = str(min(27, max(1, math.floor(constant))))
        assert row["level"] == expected_level, (
            f"level mismatch: {md5} {row['level']} != {expected_level}"
        )
        assert str(row["title"]).strip(), f"missing title: {md5}"
        assert str(row["artist"]).strip(), f"missing artist: {md5}"
        counts[row["level"]] += 1

    expected_levels = {str(level) for level in range(1, 28)}
    assert set(counts) == expected_levels, "L1-L27 must all contain charts"
    print(f"Validated {len(rows)} charts across L1-L27")


if __name__ == "__main__":
    main()
