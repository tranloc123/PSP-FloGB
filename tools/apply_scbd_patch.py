from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: apply_scbd_patch.py <ppsspp_repo>")

repo = Path(sys.argv[1]).resolve()

def read(rel):
    p = repo / rel
    if not p.exists():
        raise SystemExit(f"Missing expected PPSSPP file: {rel}")
    return p, p.read_text(encoding="utf-8")

# 1) Separate install package from stock PPSSPP while keeping Java namespace intact.
p, s = read("android/build.gradle.kts")
old = 'applicationId = "org.ppsspp.ppsspp"'
count = s.count(old)

if count < 2:
    raise SystemExit(
        f"Unexpected android/build.gradle.kts layout: "
        f"found {count} normal applicationId occurrences"
    )

s = s.replace(
    old,
    'applicationId = "com.scbd.vieweremulator"'
)

p.write_text(s, encoding="utf-8")

# 2) Android launcher name.
p, s = read("android/res/values/strings.xml")

s = s.replace(
    '<string name="app_name">PPSSPP</string>',
    '<string name="app_name">SCBD Viewer Emulator</string>'
)

s = s.replace(
    '<string name="shortcut_name">PPSSPP game</string>',
    '<string name="shortcut_name">SCBD game</string>'
)

p.write_text(s, encoding="utf-8")

# 3) Native app identity + SCBD bootstrap include.
p, s = read("UI/NativeApp.cpp")

include_anchor = '#include "ppsspp_config.h"\n'

if '#include "SCBD/SCBDViewer.h"' not in s:
    if include_anchor not in s:
        raise SystemExit("Could not find NativeApp include anchor")

    s = s.replace(
        include_anchor,
        include_anchor + '#include "SCBD/SCBDViewer.h"\n',
        1
    )

s = s.replace(
    '*app_nice_name = "PPSSPP";',
    '*app_nice_name = "SCBD Viewer Emulator";'
)

fn_anchor = (
    'void NativeGetAppInfo('
    'std::string *app_dir_name, '
    'std::string *app_nice_name, '
    'bool *landscape, '
    'std::string *version) {\n'
)

if fn_anchor not in s:
    raise SystemExit("Could not find NativeGetAppInfo")

if 'SCBDViewer::Bootstrap();' not in s:
    s = s.replace(
        fn_anchor,
        fn_anchor + '\tSCBDViewer::Bootstrap();\n',
        1
    )

p.write_text(s, encoding="utf-8")

# 4) Header-only SCBD bootstrap.
scbd = repo / "SCBD"
scbd.mkdir(exist_ok=True)

header = r'''#pragma once

#include <cstdint>

namespace SCBDViewer {

inline constexpr const char *kTargetGameId = "ULUS10457";

inline constexpr std::uint32_t kMode     = 0x08BCFE44;
inline constexpr std::uint32_t kGate     = 0x08BD034C;
inline constexpr std::uint32_t kState    = 0x08BCFCC8;
inline constexpr std::uint32_t kCombat   = 0x08BCFC90;
inline constexpr std::uint32_t kState3   = 0x08BCFC68;
inline constexpr std::uint32_t kVictory5 = 0x08BCFC50;
inline constexpr std::uint32_t kP1HP     = 0x08BE364C;
inline constexpr std::uint32_t kP2HP     = 0x08BFA30C;

inline constexpr std::uint32_t kFighterStride = 0x00016CC0;

inline void Bootstrap() noexcept {
}

}  // namespace SCBDViewer
'''

(scbd / "SCBDViewer.h").write_text(
    header,
    encoding="utf-8"
)

# 5) Build marker.
(repo / "SCBD_BUILD_INFO.txt").write_text(
    "SCBD Viewer Emulator V0.1\n"
    "Base: upstream PPSSPP master\n"
    "Target game: Soulcalibur: Broken Destiny ULUS-10457\n"
    "Milestone: custom Android fork builds/installs/runs PSP games\n",
    encoding="utf-8"
)

print("SCBD Viewer Emulator V0.1 patch applied successfully.")
