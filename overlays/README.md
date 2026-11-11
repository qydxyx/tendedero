# Local overlays

Tendedero itself is [alejandrobujan/tendedero](https://github.com/alejandrobujan/tendedero).
This fork keeps local behaviour as small overlays that are applied onto a
clean upstream tree.

Do not edit the hooked copies in `Sources/` by hand. Change the overlay,
then run:

```
python3 overlays/apply-all.py
```

## Overlays

| Directory | What it adds |
|---|---|
| `menu-bar-swipe` | Two-finger swipe down/up in the menu bar to show and hide the line, including the pin-until-visit fix |
| `space-join` | `canJoinAllApplications` so the line stays on the Space you are looking at |
| `local-build` | `swift build --build-system native` so Command Line Tools on macOS 27 still compile |

## Sync

`.github/workflows/sync-upstream.yml` fetches upstream `main` daily (and on
demand), copies this `overlays/` directory onto it, applies every overlay,
and opens a pull request. If the hooks still match, it merges. If a hook
moved, the job fails and the PR is left for a person.

After a failed apply, update the matching `apply.py` against the new
upstream file and re-run the workflow.
