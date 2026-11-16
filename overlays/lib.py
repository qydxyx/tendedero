"""Helpers for applying a Tendedero overlay onto a clean upstream tree."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys


class OverlayError(Exception):
    pass


def repo_root() -> Path:
    here = Path(__file__).resolve().parent
    return here.parent


def fail(message: str) -> None:
    raise OverlayError(message)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(repo_root())}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def already_has(path: Path, snippet: str) -> bool:
    return path.is_file() and snippet in read(path)


def replace_once(path: Path, old: str, new: str, *, label: str) -> bool:
    """Replace old with new exactly once. Skip if already applied. Return True if changed."""
    text = read(path)
    if new in text:
        return False
    count = text.count(old)
    if count == 0:
        fail(f"{label}: could not find hook in {path.relative_to(repo_root())}")
    if count > 1:
        fail(f"{label}: hook matched {count} times in {path.relative_to(repo_root())}")
    write(path, text.replace(old, new, 1))
    return True


def copy_file(src: Path, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and src.read_bytes() == dest.read_bytes():
        return False
    shutil.copy2(src, dest)
    return True


def log(message: str) -> None:
    print(message, flush=True)


def run_overlay(name: str, apply) -> int:
    try:
        changed = apply(repo_root())
        if changed:
            log(f"{name}: applied")
        else:
            log(f"{name}: already applied")
        return 0
    except OverlayError as error:
        print(f"{name}: {error}", file=sys.stderr)
        return 1
