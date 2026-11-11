#!/usr/bin/env python3
"""Use the native SwiftPM engine so Command Line Tools on macOS 27 still compile."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import replace_once, run_overlay


def apply(root: Path) -> bool:
    path = root / "scripts/build-app.sh"
    return replace_once(
        path,
        "# newest macOS 26 SDK installed alongside it.\n"
        "build_arch() {\n"
        '  local triple="$1-apple-macosx14.0"\n'
        '  if [ -z "${SDKROOT:-}" ] && ! swift build -c "$CONFIG" --triple "$triple" >&2; then\n'
        '    FALLBACK="$(ls -d /Library/Developer/CommandLineTools/SDKs/MacOSX26*.sdk 2>/dev/null | sort -V | tail -1)"\n'
        "    if [ -z \"$FALLBACK\" ]; then exit 1; fi\n"
        '    echo "Retrying with $FALLBACK" >&2\n'
        '    export SDKROOT="$FALLBACK"\n'
        "  fi\n"
        '  if [ -n "${SDKROOT:-}" ]; then swift build -c "$CONFIG" --triple "$triple" >&2; fi\n'
        '  cp "$(swift build -c "$CONFIG" --triple "$triple" --show-bin-path)/Tendedero" "$OUT/Tendedero-$1"\n'
        "}\n",
        "# newest macOS 26 SDK installed alongside it. The default swiftbuild engine\n"
        '# also fails to start on those tools ("Unknown error parsing property list");\n'
        "# --build-system native is the llbuild path that still compiles.\n"
        "build_arch() {\n"
        '  local triple="$1-apple-macosx14.0"\n'
        "  local extra=(--build-system native)\n"
        '  if [ -z "${SDKROOT:-}" ] && ! swift build -c "$CONFIG" --triple "$triple" "${extra[@]}" >&2; then\n'
        '    FALLBACK="$(ls -d /Library/Developer/CommandLineTools/SDKs/MacOSX26*.sdk 2>/dev/null | sort -V | tail -1)"\n'
        "    if [ -z \"$FALLBACK\" ]; then exit 1; fi\n"
        '    echo "Retrying with $FALLBACK" >&2\n'
        '    export SDKROOT="$FALLBACK"\n'
        "  fi\n"
        '  if [ -n "${SDKROOT:-}" ]; then swift build -c "$CONFIG" --triple "$triple" "${extra[@]}" >&2; fi\n'
        '  cp "$(swift build -c "$CONFIG" --triple "$triple" "${extra[@]}" --show-bin-path)/Tendedero" "$OUT/Tendedero-$1"\n'
        "}\n",
        label="build-app.sh native engine",
    )


if __name__ == "__main__":
    sys.exit(run_overlay("local-build", apply))
