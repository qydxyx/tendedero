#!/usr/bin/env python3
"""Keep the line joinable to every Space, including after a Space switch."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import replace_once, run_overlay

BEHAVIOR = "[.canJoinAllSpaces, .stationary, .ignoresCycle, .fullScreenAuxiliary]"
BEHAVIOR_JOIN = "[.canJoinAllSpaces, .stationary, .ignoresCycle, .fullScreenAuxiliary, .canJoinAllApplications]"


def apply(root: Path) -> bool:
    panel = root / "Sources/Tendedero/LinePanel.swift"
    flight = root / "Sources/Tendedero/CaptureFlight.swift"
    delegate = root / "Sources/Tendedero/AppDelegate.swift"
    changed = False
    changed |= replace_once(
        panel,
        f"        collectionBehavior = {BEHAVIOR}\n",
        f"        collectionBehavior = {BEHAVIOR_JOIN}\n",
        label="LinePanel collectionBehavior",
    )
    changed |= replace_once(
        panel,
        "        } else {\n"
        "            super.sendEvent(event)\n"
        "        }\n"
        "    }\n"
        "\n"
        "    override var canBecomeKey: Bool { false }\n",
        "        } else {\n"
        "            super.sendEvent(event)\n"
        "        }\n"
        "    }\n"
        "\n"
        "    override func orderFrontRegardless() {\n"
        f"        collectionBehavior = {BEHAVIOR_JOIN}\n"
        "        super.orderFrontRegardless()\n"
        "    }\n"
        "\n"
        "    override var canBecomeKey: Bool { false }\n",
        label="LinePanel orderFrontRegardless",
    )
    changed |= replace_once(
        panel,
        "        if frame != target { setFrame(target, display: true) }\n"
        "    }\n"
        "}\n",
        "        if frame != target { setFrame(target, display: true) }\n"
        f"        collectionBehavior = {BEHAVIOR_JOIN}\n"
        "    }\n"
        "}\n",
        label="LinePanel placeOnScreen",
    )
    changed |= replace_once(
        flight,
        f"        window.collectionBehavior = {BEHAVIOR}\n",
        f"        window.collectionBehavior = {BEHAVIOR_JOIN}\n",
        label="CaptureFlight collectionBehavior",
    )
    changed |= replace_once(
        delegate,
        "                    if name == NSWorkspace.activeSpaceDidChangeNotification { self?.openedOnPurpose = false }\n",
        "                    if name == NSWorkspace.activeSpaceDidChangeNotification {\n"
        "                        self?.openedOnPurpose = false\n"
        "                        self?.menuBarSuppressed = false\n"
        "                        self?.hotZoneSince = nil\n"
        "                        self?.panel.placeOnScreen()\n"
        "                    }\n",
        label="active Space switch",
    )
    return changed


if __name__ == "__main__":
    sys.exit(run_overlay("space-join", apply))
