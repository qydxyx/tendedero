# menu-bar-swipe

Two-finger swipe down in the menu bar brings the line down and pins it.
Swipe up puts it away. One switch, on by default, under Bring the line down.

`MenuBarSwipe.swift` is the whole gesture engine. It does not call into
AppDelegate. `apply.py` copies that file into `Sources/Tendedero` and
inserts a few hooks:

- the `menuBarSwipe` property and `swipeFromMenuBar` preference
- `watchMenuBarSwipe()` at launch
- `revealFromSwipe` / `hideFromSwipe`
- the menu item
- translations and README rows
- the pin fix: `tick()` only clears `pinned` when the pointer is over the
  photos, not while it is still in the menu bar
