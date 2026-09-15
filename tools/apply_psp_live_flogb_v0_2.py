from pathlib import Path
import sys

try:
    from PIL import Image
except Exception as e:
    raise SystemExit("Pillow is required. Workflow should install it first: " + str(e))

if len(sys.argv) != 3:
    raise SystemExit(
        "Usage: apply_psp_live_flogb_v0_2.py <ppsspp_repo> <icon_source.png>"
    )

repo = Path(sys.argv[1]).resolve()
icon_source = Path(sys.argv[2]).resolve()

TARGET_GAME_ID = "ULUS10457"
APP_NAME = "PSP Live FloGB"
APPLICATION_ID = "com.scbd.vieweremulator"

def require(rel):
    p = repo / rel
    if not p.exists():
        raise SystemExit(f"Missing expected PPSSPP path: {rel}")
    return p

def read(rel):
    p = require(rel)
    return p, p.read_text(encoding="utf-8")

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"{label}: expected exactly 1 occurrence, found {count}"
        )
    return text.replace(old, new, 1)

# ================================================================
# 1) Android identity
# ================================================================
p, s = read("android/build.gradle.kts")

old_app_id = 'applicationId = "org.ppsspp.ppsspp"'
count = s.count(old_app_id)
if count != 2:
    raise SystemExit(
        f"android/build.gradle.kts: expected 2 normal applicationId entries, found {count}"
    )

s = s.replace(
    old_app_id,
    f'applicationId = "{APPLICATION_ID}"'
)
p.write_text(s, encoding="utf-8")

p, s = read("android/res/values/strings.xml")
s = replace_once(
    s,
    '<string name="app_name">PPSSPP</string>',
    f'<string name="app_name">{APP_NAME}</string>',
    "strings.xml app_name"
)
s = replace_once(
    s,
    '<string name="shortcut_name">PPSSPP game</string>',
    f'<string name="shortcut_name">{APP_NAME}</string>',
    "strings.xml shortcut_name"
)
p.write_text(s, encoding="utf-8")

p, s = read("UI/NativeApp.cpp")
s = replace_once(
    s,
    '*app_nice_name = "PPSSPP";',
    f'*app_nice_name = "{APP_NAME}";',
    "NativeApp.cpp app nice name"
)
p.write_text(s, encoding="utf-8")

# ================================================================
# 2) Launcher icon
# ================================================================
if not icon_source.exists():
    raise SystemExit(f"Icon source not found: {icon_source}")

im = Image.open(icon_source).convert("RGB")
iw, ih = im.size
side = min(iw, ih)
x0 = (iw - side) // 2
y0 = (ih - side) // 2
im = im.crop((x0, y0, x0 + side, y0 + side))

launcher_sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}
foreground_sizes = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}

for folder, px in launcher_sizes.items():
    d = require(f"android/normal/res/{folder}")
    resized = im.resize((px, px), Image.Resampling.LANCZOS)
    resized.save(d / "ic_launcher.png", "PNG", optimize=True)
    resized.save(d / "ic_launcher_round.png", "PNG", optimize=True)

for folder, px in foreground_sizes.items():
    d = require(f"android/normal/res/{folder}")
    resized = im.resize((px, px), Image.Resampling.LANCZOS)
    resized.save(d / "ic_launcher_foreground.png", "PNG", optimize=True)

p, s = read("android/normal/res/values/ic_launcher_background.xml")
s = s.replace("#2D4553", "#26070D")
p.write_text(s, encoding="utf-8")

# ================================================================
# 3) SCBD native memory module
# ================================================================
scbd_dir = repo / "SCBD"
scbd_dir.mkdir(exist_ok=True)

header = r'''#pragma once

#include "Core/MemMap.h"

namespace SCBDViewer {

inline constexpr const char *kTargetGameId = "ULUS10457";

inline constexpr u32 kMode     = 0x08BCFE44;
inline constexpr u32 kGate     = 0x08BD034C;
inline constexpr u32 kState    = 0x08BCFCC8;
inline constexpr u32 kCombat   = 0x08BCFC90;
inline constexpr u32 kState3   = 0x08BCFC68;
inline constexpr u32 kVictory5 = 0x08BCFC50;
inline constexpr u32 kP1HP     = 0x08BE364C;
inline constexpr u32 kP2HP     = 0x08BFA30C;
inline constexpr u32 kFighterStride = 0x00016CC0;

struct Snapshot {
    bool readable = false;

    u32 p1HP = 0;
    u32 p2HP = 0;
    float p1HPFloat = 0.0f;
    float p2HPFloat = 0.0f;

    u32 mode = 0;
    u32 gate = 0;
    u32 state = 0;
    u32 combat = 0;
    u32 state3 = 0;
    u32 victory5 = 0;
};

inline bool CanRead32(u32 address) {
    return Memory::IsActive() &&
           Memory::IsValid4AlignedAddress(address);
}

inline bool CoreAddressesReadable() {
    return CanRead32(kP1HP) &&
           CanRead32(kP2HP) &&
           CanRead32(kMode) &&
           CanRead32(kGate) &&
           CanRead32(kState) &&
           CanRead32(kCombat) &&
           CanRead32(kState3) &&
           CanRead32(kVictory5);
}

inline u32 ReadU32(u32 address) {
    if (!CanRead32(address))
        return 0;
    return Memory::ReadUnchecked_U32(address);
}

inline float ReadFloat(u32 address) {
    if (!CanRead32(address))
        return 0.0f;
    return Memory::ReadUnchecked_Float(address);
}

inline Snapshot ReadSnapshot() {
    Snapshot s{};
    s.readable = CoreAddressesReadable();

    if (!s.readable)
        return s;

    s.p1HP = ReadU32(kP1HP);
    s.p2HP = ReadU32(kP2HP);
    s.p1HPFloat = ReadFloat(kP1HP);
    s.p2HPFloat = ReadFloat(kP2HP);

    s.mode = ReadU32(kMode);
    s.gate = ReadU32(kGate);
    s.state = ReadU32(kState);
    s.combat = ReadU32(kCombat);
    s.state3 = ReadU32(kState3);
    s.victory5 = ReadU32(kVictory5);

    return s;
}

}  // namespace SCBDViewer
'''
(scbd_dir / "SCBDViewer.h").write_text(header, encoding="utf-8")

# ================================================================
# 4) Native in-emulator HUD
# ================================================================
p, s = read("UI/DebugOverlay.h")
anchor = 'void DrawFPS(UIContext *ctx, const Bounds &bounds);\n'
if anchor not in s:
    raise SystemExit("DebugOverlay.h: DrawFPS declaration anchor missing")

if "DrawSCBDOverlay" not in s:
    s = s.replace(
        anchor,
        anchor +
        'bool ShouldDrawSCBDOverlay();\n'
        'void DrawSCBDOverlay(UIContext *ctx, const Bounds &bounds);\n',
        1
    )
p.write_text(s, encoding="utf-8")

p, s = read("UI/DebugOverlay.cpp")

include_anchor = '#include "Core/ELF/ParamSFO.h"\n'
if include_anchor not in s:
    raise SystemExit("DebugOverlay.cpp: ParamSFO include anchor missing")

if '#include "SCBD/SCBDViewer.h"' not in s:
    s = s.replace(
        include_anchor,
        include_anchor + '#include "SCBD/SCBDViewer.h"\n',
        1
    )

drawfps_anchor = 'void DrawFPS(UIContext *ctx, const Bounds &bounds) {\n'
if drawfps_anchor not in s:
    raise SystemExit("DebugOverlay.cpp: DrawFPS anchor missing")

scbd_overlay = r'''bool ShouldDrawSCBDOverlay() {
    if (!PSP_IsInited())
        return false;

    if (g_paramSFO.GetDiscID() != SCBDViewer::kTargetGameId)
        return false;

    return SCBDViewer::CoreAddressesReadable();
}

void DrawSCBDOverlay(UIContext *ctx, const Bounds &bounds) {
    if (!ShouldDrawSCBDOverlay())
        return;

    const SCBDViewer::Snapshot snap = SCBDViewer::ReadSnapshot();
    if (!snap.readable)
        return;

    FontID ubuntu24("UBUNTU24");

    char text[1024];
    snprintf(
        text,
        sizeof(text),
        "PSP Live FloGB | SCBD V0.2\n"
        "ULUS10457 | NATIVE RAM: OK\n"
        "P1 HP  U32:%u  HEX:%08X  F:%0.2f\n"
        "P2 HP  U32:%u  HEX:%08X  F:%0.2f\n"
        "MODE:%08X  GATE:%08X\n"
        "STATE:%08X  COMBAT:%08X\n"
        "STATE3:%08X  VICTORY:%08X",
        snap.p1HP, snap.p1HP, snap.p1HPFloat,
        snap.p2HP, snap.p2HP, snap.p2HPFloat,
        snap.mode, snap.gate,
        snap.state, snap.combat,
        snap.state3, snap.victory5
    );

    ctx->Flush();
    ctx->BindFontTexture();
    ctx->Draw()->SetFontScale(0.50f, 0.50f);

    const float x = bounds.x + 14.0f;
    const float y = bounds.y + 54.0f;
    const float width = std::min(bounds.w * 0.62f, 720.0f);
    const float height = 230.0f;

    ctx->Draw()->DrawTextRect(
        ubuntu24,
        text,
        x + 2.0f,
        y + 2.0f,
        width,
        height,
        0xD0000000,
        FLAG_DYNAMIC_ASCII
    );

    ctx->Draw()->DrawTextRect(
        ubuntu24,
        text,
        x,
        y,
        width,
        height,
        0xFF66FF88,
        FLAG_DYNAMIC_ASCII
    );

    ctx->Draw()->SetFontScale(1.0f, 1.0f);
    ctx->Flush();
    ctx->RebindTexture();
}

'''

if "bool ShouldDrawSCBDOverlay()" not in s:
    s = s.replace(
        drawfps_anchor,
        scbd_overlay + drawfps_anchor,
        1
    )

p.write_text(s, encoding="utf-8")

# ================================================================
# 5) Make EmuScreen render the SCBD HUD every game frame
# ================================================================
p, s = read("UI/EmuScreen.cpp")

visible_anchor = '''bool EmuScreen::hasVisibleUI() {
\t// Regular but uncommon UI.
'''
if visible_anchor not in s:
    raise SystemExit("EmuScreen.cpp: hasVisibleUI anchor missing")

prefix_before_renderui = s.split("void EmuScreen::renderUI()", 1)[0]
if "ShouldDrawSCBDOverlay()" not in prefix_before_renderui:
    s = s.replace(
        visible_anchor,
        '''bool EmuScreen::hasVisibleUI() {
\tif (ShouldDrawSCBDOverlay())
\t\treturn true;

\t// Regular but uncommon UI.
''',
        1
    )

render_anchor = '''\t\tif (g_Config.iShowStatusFlags) {
\t\t\tDrawFPS(ctx, GetLayoutBounds(*ctx));
\t\t}
'''
if render_anchor not in s:
    raise SystemExit("EmuScreen.cpp: renderUI FPS anchor missing")

if "DrawSCBDOverlay(ctx" not in s:
    s = s.replace(
        render_anchor,
        render_anchor +
        '''\t\tif (ShouldDrawSCBDOverlay()) {
\t\t\tDrawSCBDOverlay(ctx, GetLayoutBounds(*ctx));
\t\t}
''',
        1
    )

p.write_text(s, encoding="utf-8")

# ================================================================
# 6) Build marker
# ================================================================
(repo / "PSP_LIVE_FLOGB_BUILD_INFO.txt").write_text(
    "PSP Live FloGB V0.2\n"
    "Target: Soulcalibur Broken Destiny ULUS-10457\n"
    "Feature: native PSP RAM reader + in-emulator debug HUD\n"
    "Package: com.scbd.vieweremulator (kept for V0.1 update compatibility)\n"
    "Branding: PSP Live FloGB + custom launcher icon\n",
    encoding="utf-8"
)

print("PSP Live FloGB V0.2 patch applied successfully.")
