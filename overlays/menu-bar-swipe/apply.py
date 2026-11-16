#!/usr/bin/env python3
"""Copy MenuBarSwipe.swift and hook it into a clean upstream Tendedero tree."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import already_has, copy_file, fail, read, replace_once, run_overlay, write

SWIPE_KEY = "When the pointer swipes down or up"

# English key → translation. Unknown locales fall back to English.
STRINGS = {
    "az": "Göstərici aşağı və ya yuxarı sürüşdürüləndə",
    "en": SWIPE_KEY,
    "es": "Al deslizar el puntero hacia abajo o hacia arriba",
    "fr": "Quand le pointeur glisse vers le bas ou vers le haut",
    "gl": "Ao esvarar o punteiro cara abaixo ou cara arriba",
    "hi": "जब पॉइंटर नीचे या ऊपर स्वाइप करे",
    "it": "Quando il puntatore scorre in basso o in alto",
    "ja": "ポインタを上下にスワイプしたとき",
    "ko": "포인터를 아래나 위로 쓸 때",
    "pt-BR": "Quando o ponteiro desliza para baixo ou para cima",
    "tr": "İşaretçi aşağı veya yukarı kaydırıldığında",
    "vi": "Khi con trỏ vuốt xuống hoặc lên",
    "zh-Hans": "指针上下滑动时",
}

# Insert the two swipe rows immediately after this hover row.
README_ROWS = {
    "README.md": (
        "| Rest the pointer in the middle of the menu bar | Bring the line down on that screen. |",
        "| Two-finger swipe down in the menu bar | Bring the line down on that screen, and keep it there. |\n"
        "| Two-finger swipe up in the menu bar | Put it away. |",
    ),
    "docs/i18n/README.az.md": (
        "| Göstəricini menyu panelinin ortasında saxlamaq | İpi həmin ekranda endirir. |",
        "| Menyu panelində iki barmaqla aşağı sürüşdürmək | İpi həmin ekranda endirir və orada saxlayır. |\n"
        "| Menyu panelində iki barmaqla yuxarı sürüşdürmək | İpi yığır. |",
    ),
    "docs/i18n/README.es.md": (
        "| Dejar el puntero en el centro de la barra de menús | Baja la cuerda en esa pantalla. |",
        "| Deslizar dos dedos hacia abajo en la barra de menús | Baja la cuerda en esa pantalla y la deja ahí. |\n"
        "| Deslizar dos dedos hacia arriba en la barra de menús | Recoge la cuerda. |",
    ),
    "docs/i18n/README.fr.md": (
        "| Poser le pointeur au milieu de la barre des menus | Fait descendre la corde sur cet écran. |",
        "| Balayer vers le bas à deux doigts dans la barre des menus | Fait descendre la corde sur cet écran et la laisse. |\n"
        "| Balayer vers le haut à deux doigts dans la barre des menus | Range la corde. |",
    ),
    "docs/i18n/README.gl.md": (
        "| Deixar o punteiro no centro da barra de menús | Baixa a corda nesa pantalla. |",
        "| Esvarar dous dedos cara abaixo na barra de menús | Baixa a corda nesa pantalla e déixaa aí. |\n"
        "| Esvarar dous dedos cara arriba na barra de menús | Recolle a corda. |",
    ),
    "docs/i18n/README.hi.md": (
        "| पॉइंटर को मेनू बार के बीच में रोकें | उस स्क्रीन पर रस्सी नीचे लाएँ। |",
        "| मेनू बार में दो उँगलियों से नीचे स्वाइप करें | उस स्क्रीन पर रस्सी नीचे लाएँ और वहीं रखें। |\n"
        "| मेनू बार में दो उँगलियों से ऊपर स्वाइप करें | रस्सी ऊपर कर दें। |",
    ),
    "docs/i18n/README.it.md": (
        "| Fermare il puntatore al centro della barra dei menu | Fa scendere il filo su quello schermo. |",
        "| Scorrere due dita verso il basso nella barra dei menu | Fa scendere il filo su quello schermo e lo lascia. |\n"
        "| Scorrere due dita verso l'alto nella barra dei menu | Ritira il filo. |",
    ),
    "docs/i18n/README.ja.md": (
        "| メニューバーの中央にポインタを置く | その画面にロープを降ろす。 |",
        "| メニューバーで二本指下スワイプ | その画面にロープを降ろし、出したままにする。 |\n"
        "| メニューバーで二本指上スワイプ | ロープをしまう。 |",
    ),
    "docs/i18n/README.ko.md": (
        "| 포인터를 메뉴 막대 가운데에 올려 두기 | 그 화면에 빨랫줄을 내려요. |",
        "| 메뉴 막대에서 두 손가락으로 아래로 쓸기 | 그 화면에 빨랫줄을 내리고 그대로 둬요. |\n"
        "| 메뉴 막대에서 두 손가락으로 위로 쓸기 | 빨랫줄을 치워요. |",
    ),
    "docs/i18n/README.pt-BR.md": (
        "| Parar o ponteiro no meio da barra de menus | Baixa o varal naquela tela. |",
        "| Deslizar dois dedos para baixo na barra de menus | Baixa o varal naquela tela e o deixa lá. |\n"
        "| Deslizar dois dedos para cima na barra de menus | Recolhe o varal. |",
    ),
    "docs/i18n/README.tr.md": (
        "| İşaretçiyi menü çubuğunun ortasında bırak | O ekranda ipi aşağı indirir. |",
        "| Menü çubuğunda iki parmakla aşağı kaydır | O ekranda ipi aşağı indirir ve orada tutar. |\n"
        "| Menü çubuğunda iki parmakla yukarı kaydır | İpi geri kaldırır. |",
    ),
    "docs/i18n/README.vi.md": (
        "| Đặt con trỏ ở giữa thanh menu | Kéo dây phơi xuống trên màn hình đó. |",
        "| Vuốt hai ngón xuống trên thanh menu | Kéo dây phơi xuống trên màn hình đó và giữ nguyên. |\n"
        "| Vuốt hai ngón lên trên thanh menu | Thu gọn dây phơi. |",
    ),
    "docs/i18n/README.zh-Hans.md": (
        "| 指针停在菜单栏中间 | 在那一块屏幕上放下绳子。 |",
        "| 在菜单栏双指向下滑动 | 在那一块屏幕上放下绳子，并留着。 |\n"
        "| 在菜单栏双指向上滑动 | 把绳子收起来。 |",
    ),
}

SWIPE_METHODS = '''
    private func watchMenuBarSwipe() {
        let swipe = MenuBarSwipe()
        swipe.isEnabled = { AppDelegate.swipeFromMenuBar }
        swipe.onSwipe = { [weak self] direction, screen in
            switch direction {
            case .down: self?.revealFromSwipe(on: screen)
            case .up: self?.hideFromSwipe()
            }
        }
        swipe.start()
        menuBarSwipe = swipe
    }

    /// A two-finger swipe down from the menu bar, like opening the line on
    /// purpose with the shortcut. It stays until the pointer has visited the
    /// photos and left. Occupying the menu bar does not count as a visit.
    /// Already down, it only pins.
    private func revealFromSwipe(on screen: NSScreen) {
        guard !FullScreen.blocksLine(on: screen) else { return }
        menuBarSuppressed = false
        if isRevealed {
            pinned = true
            return
        }
        keepOpen = true
        wanted = true
        openedOnPurpose = true
        panel.placeOnScreen(screen)
        updateCapacity()
        refresh()
        reveal(pinned: true)
    }

    /// Swipe up from the menu bar tucks the line away. The pointer is still
    /// in the menu bar, so hover is held off until it leaves, as after a
    /// click there.
    private func hideFromSwipe() {
        guard isRevealed else { return }
        menuBarSuppressed = true
        hotZoneSince = nil
        setRevealed(false)
    }

'''


def apply_app_delegate(root: Path) -> bool:
    path = root / "Sources/Tendedero/AppDelegate.swift"
    changed = False
    changed |= replace_once(
        path,
        "    private var hotKey: HotKey?\n"
        "    /// ⌃⌥F searches the line. Fixed, apart from the shortcut that shows it.\n",
        "    private var hotKey: HotKey?\n"
        "    private var menuBarSwipe: MenuBarSwipe?\n"
        "    /// ⌃⌥F searches the line. Fixed, apart from the shortcut that shows it.\n",
        label="menuBarSwipe property",
    )
    changed |= replace_once(
        path,
        "    // What brings the line down, from the menu bar's \"Bring the line down\".\n"
        "    // Out of the box, the first two are on and the third off.\n"
        "\n"
        "    /// Resting the pointer in the menu bar. Off, only the shortcut and the\n"
        "    /// menu open it.\n"
        "    static var opensFromMenuBar: Bool {\n"
        "        get { !UserDefaults.standard.bool(forKey: \"menuBarRevealOff\") }\n"
        "        set { UserDefaults.standard.set(!newValue, forKey: \"menuBarRevealOff\") }\n"
        "    }\n"
        "\n"
        "    /// Something new hanging shows itself for a moment. Off, it hangs\n",
        "    // What brings the line down, from the menu bar's \"Bring the line down\".\n"
        "    // Out of the box, the first three are on and the last off.\n"
        "\n"
        "    /// Resting the pointer in the menu bar. Off, only the shortcut, a\n"
        "    /// swipe, and the menu open it.\n"
        "    static var opensFromMenuBar: Bool {\n"
        "        get { !UserDefaults.standard.bool(forKey: \"menuBarRevealOff\") }\n"
        "        set { UserDefaults.standard.set(!newValue, forKey: \"menuBarRevealOff\") }\n"
        "    }\n"
        "\n"
        "    /// Two-finger swipe down in the menu bar brings the line down; swipe\n"
        "    /// up puts it away. Same switch.\n"
        "    static var swipeFromMenuBar: Bool {\n"
        "        get { !UserDefaults.standard.bool(forKey: \"menuBarSwipeOff\") }\n"
        "        set { UserDefaults.standard.set(!newValue, forKey: \"menuBarSwipeOff\") }\n"
        "    }\n"
        "\n"
        "    /// Something new hanging shows itself for a moment. Off, it hangs\n",
        label="swipeFromMenuBar preference",
    )
    changed |= replace_once(
        path,
        "        setUpStatusItem()\n"
        "        watchMenuBarClicks()\n"
        "        watchPutBackKey()\n",
        "        setUpStatusItem()\n"
        "        watchMenuBarClicks()\n"
        "        watchMenuBarSwipe()\n"
        "        watchPutBackKey()\n",
        label="watchMenuBarSwipe() call",
    )
    changed |= replace_once(
        path,
        "            // An empty line stays up there: only the shortcut and the menu\n"
        "            // bring it down on purpose.\n",
        "            // An empty line stays up there: only the shortcut, a swipe, and\n"
        "            // the menu bring it down on purpose.\n",
        label="empty-line comment",
    )
    changed |= replace_once(
        path,
        "    /// How long the cursor is away before the line tucks back up.\n"
        "    private static let retractDelay: TimeInterval = 0.5\n",
        SWIPE_METHODS
        + "    /// How long the cursor is away before the line tucks back up.\n"
        + "    private static let retractDelay: TimeInterval = 0.5\n",
        label="swipe methods",
    )
    changed |= replace_once(
        path,
        "        if inside && pinned && !searching { pinned = false }\n",
        "        // Occupying the menu bar is not a visit to the line. A swipe-down\n"
        "        // (or the shortcut) while the pointer is still there stays pinned\n"
        "        // until the pointer has been over the photos, or an explicit hide.\n"
        "        if inside && !inMenuBar && pinned && !searching { pinned = false }\n",
        label="pin until a real visit",
    )
    changed |= replace_once(
        path,
        "        hover.state = Self.opensFromMenuBar ? .on : .off\n"
        "        options.addItem(hover)\n"
        "        let peek = ClosureMenuItem(L(\"When something new hangs\")) {\n",
        "        hover.state = Self.opensFromMenuBar ? .on : .off\n"
        "        options.addItem(hover)\n"
        "        let swipe = ClosureMenuItem(L(\"When the pointer swipes down or up\")) {\n"
        "            AppDelegate.swipeFromMenuBar.toggle()\n"
        "        }\n"
        "        swipe.state = Self.swipeFromMenuBar ? .on : .off\n"
        "        options.addItem(swipe)\n"
        "        let peek = ClosureMenuItem(L(\"When something new hangs\")) {\n",
        label="swipe menu item",
    )
    return changed


def apply_strings(root: Path) -> bool:
    changed = False
    resources = root / "Sources/Tendedero/Resources"
    if not resources.is_dir():
        fail("Sources/Tendedero/Resources is missing")
    hover = '"When the pointer rests in the menu bar"'
    for folder in sorted(resources.glob("*.lproj")):
        locale = folder.name.removesuffix(".lproj")
        path = folder / "Localizable.strings"
        text = read(path)
        if f'"{SWIPE_KEY}"' in text:
            continue
        translation = STRINGS.get(locale, STRINGS["en"])
        line = f'"{SWIPE_KEY}" = "{translation}";\n'
        inserted = False
        out = []
        for existing in text.splitlines(keepends=True):
            out.append(existing)
            if existing.startswith(hover):
                out.append(line)
                inserted = True
        if not inserted:
            fail(f"{path.relative_to(root)}: no hover string to insert after")
        write(path, "".join(out))
        changed = True
    return changed


def apply_readmes(root: Path) -> bool:
    changed = False
    for relative, (anchor, rows) in README_ROWS.items():
        path = root / relative
        if not path.is_file():
            continue
        if rows.split("\n", 1)[0] in read(path):
            continue
        if not replace_once(path, anchor + "\n", anchor + "\n" + rows + "\n", label=relative):
            continue
        changed = True
    return changed


def apply(root: Path) -> bool:
    src = Path(__file__).resolve().parent / "MenuBarSwipe.swift"
    dest = root / "Sources/Tendedero/MenuBarSwipe.swift"
    changed = copy_file(src, dest)
    changed |= apply_app_delegate(root)
    changed |= apply_strings(root)
    changed |= apply_readmes(root)
    if not already_has(root / "Sources/Tendedero/AppDelegate.swift", "watchMenuBarSwipe()"):
        fail("AppDelegate.swift is missing watchMenuBarSwipe() after apply")
    return changed


if __name__ == "__main__":
    sys.exit(run_overlay("menu-bar-swipe", apply))
