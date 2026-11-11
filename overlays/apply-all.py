#!/usr/bin/env python3
"""Apply every overlay in overlays/*/apply.py onto the current tree.

Run from the repo root, or from anywhere: python3 overlays/apply-all.py.
Overlays run in directory-name order.
"""

from __future__ import annotations

from pathlib import Path
import runpy
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lib import OverlayError, log, run_overlay  # noqa: E402


def overlay_scripts() -> list[Path]:
    return sorted(path for path in HERE.glob("*/apply.py") if path.is_file())


def main() -> int:
    scripts = overlay_scripts()
    if not scripts:
        print("no overlays found", file=sys.stderr)
        return 1
    failed = 0
    for script in scripts:
        name = script.parent.name
        log(f"applying {name}")
        try:
            ns = runpy.run_path(str(script), run_name="overlay_apply")
            apply = ns.get("apply")
            if apply is None:
                print(f"{name}: apply.py has no apply()", file=sys.stderr)
                failed += 1
                continue
            if run_overlay(name, apply) != 0:
                failed += 1
        except OverlayError as error:
            print(f"{name}: {error}", file=sys.stderr)
            failed += 1
    if failed:
        print(f"{failed} overlay(s) failed", file=sys.stderr)
        return 1
    log("all overlays applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
