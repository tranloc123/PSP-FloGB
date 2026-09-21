from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: apply_psp_live_flogb_v0_5_8c.py <ppsspp_repo>")

repo = Path(sys.argv[1]).resolve()

def require(rel):
    p = repo / rel
    if not p.exists():
        raise SystemExit(f"Missing expected path: {rel}")
    return p

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 occurrence, found {count}")
    return text.replace(old, new, 1)

def replace_between(text, start, end, replacement, label):
    a = text.find(start)
    if a < 0:
        raise SystemExit(f"{label}: start marker missing")
    b = text.find(end, a + len(start))
    if b < 0:
        raise SystemExit(f"{label}: end marker missing")
    return text[:a] + replacement + "\n\n" + text[b:]

debug = require("UI/DebugOverlay.cpp")
info = require("PSP_LIVE_FLOGB_BUILD_INFO.txt")

for rel in (
    "assets/scbd/characters/character_portraits_atlas.png",
    "assets/scbd/winner_asset_v058c/pick_portraits_exact.png",
    "assets/scbd/winner_asset_v058c/royal_unicode_atlas.png",
    "assets/scbd/winner_asset_v058c/timer_digits.png",
):
    require(rel)

s = debug.read_text(encoding="utf-8")

for marker in (
    "WINNER FINAL V0.5.7C4R1",
    "DrawSCBDTransparentTop5List",
    "DrawSCBDRankAvatar",
    "DrawSCBDCharacterPortraitSlot",
    "Approved Top Character layout",
    "DrawSCBDMatchTop5HUD",
    "SCBDVirtualInput::Process();",
):
    if marker not in s:
        raise SystemExit(f"V0.5.8C prerequisite missing: {marker}")

royal_helper = '\n// -----------------------------------------------------------------------------\n// V0.5.8C Royal Unicode / Numeral Texture Engine\n// Fixed raster assets, UTF-8 decoder, safe fallback, no PPSSPP DrawText for\n// Winner/Ranking/Top5 production text.\n// -----------------------------------------------------------------------------\nstatic Draw::Texture *g_scbdRoyalUnicodeAtlasV058C = nullptr;\nstatic bool g_scbdRoyalUnicodeAtlasV058CAttempted = false;\nstatic Draw::Texture *g_scbdTimerAtlasV058C = nullptr;\nstatic bool g_scbdTimerAtlasV058CAttempted = false;\n\nstatic constexpr int kSCBDRoyalColsV058C = 16;\nstatic constexpr int kSCBDRoyalCellWV058C = 80;\nstatic constexpr int kSCBDRoyalCellHV058C = 96;\nstatic constexpr int kSCBDRoyalAtlasWV058C = 1280;\nstatic constexpr int kSCBDRoyalAtlasHV058C = 2016;\nstatic constexpr int kSCBDRoyalGlyphCountV058C = 329;\n\nstatic const uint32_t kSCBDRoyalCodepointsV058C[kSCBDRoyalGlyphCountV058C] = {\n    0x0020u, 0x0021u, 0x0022u, 0x0023u, 0x0024u, 0x0025u, 0x0026u, 0x0027u, 0x0028u, 0x0029u,\n    0x002Au, 0x002Bu, 0x002Cu, 0x002Du, 0x002Eu, 0x002Fu, 0x0030u, 0x0031u, 0x0032u, 0x0033u,\n    0x0034u, 0x0035u, 0x0036u, 0x0037u, 0x0038u, 0x0039u, 0x003Au, 0x003Bu, 0x003Cu, 0x003Du,\n    0x003Eu, 0x003Fu, 0x0040u, 0x0041u, 0x0042u, 0x0043u, 0x0044u, 0x0045u, 0x0046u, 0x0047u,\n    0x0048u, 0x0049u, 0x004Au, 0x004Bu, 0x004Cu, 0x004Du, 0x004Eu, 0x004Fu, 0x0050u, 0x0051u,\n    0x0052u, 0x0053u, 0x0054u, 0x0055u, 0x0056u, 0x0057u, 0x0058u, 0x0059u, 0x005Au, 0x005Bu,\n    0x005Cu, 0x005Du, 0x005Eu, 0x005Fu, 0x0060u, 0x0061u, 0x0062u, 0x0063u, 0x0064u, 0x0065u,\n    0x0066u, 0x0067u, 0x0068u, 0x0069u, 0x006Au, 0x006Bu, 0x006Cu, 0x006Du, 0x006Eu, 0x006Fu,\n    0x0070u, 0x0071u, 0x0072u, 0x0073u, 0x0074u, 0x0075u, 0x0076u, 0x0077u, 0x0078u, 0x0079u,\n    0x007Au, 0x007Bu, 0x007Cu, 0x007Du, 0x007Eu, 0x00A0u, 0x00A1u, 0x00A2u, 0x00A3u, 0x00A4u,\n    0x00A5u, 0x00A6u, 0x00A7u, 0x00A8u, 0x00A9u, 0x00AAu, 0x00ABu, 0x00ACu, 0x00ADu, 0x00AEu,\n    0x00AFu, 0x00B0u, 0x00B1u, 0x00B2u, 0x00B3u, 0x00B4u, 0x00B5u, 0x00B6u, 0x00B7u, 0x00B8u,\n    0x00B9u, 0x00BAu, 0x00BBu, 0x00BCu, 0x00BDu, 0x00BEu, 0x00BFu, 0x00C0u, 0x00C1u, 0x00C2u,\n    0x00C3u, 0x00C4u, 0x00C5u, 0x00C6u, 0x00C7u, 0x00C8u, 0x00C9u, 0x00CAu, 0x00CBu, 0x00CCu,\n    0x00CDu, 0x00CEu, 0x00CFu, 0x00D0u, 0x00D1u, 0x00D2u, 0x00D3u, 0x00D4u, 0x00D5u, 0x00D6u,\n    0x00D7u, 0x00D8u, 0x00D9u, 0x00DAu, 0x00DBu, 0x00DCu, 0x00DDu, 0x00DEu, 0x00DFu, 0x00E0u,\n    0x00E1u, 0x00E2u, 0x00E3u, 0x00E4u, 0x00E5u, 0x00E6u, 0x00E7u, 0x00E8u, 0x00E9u, 0x00EAu,\n    0x00EBu, 0x00ECu, 0x00EDu, 0x00EEu, 0x00EFu, 0x00F0u, 0x00F1u, 0x00F2u, 0x00F3u, 0x00F4u,\n    0x00F5u, 0x00F6u, 0x00F7u, 0x00F8u, 0x00F9u, 0x00FAu, 0x00FBu, 0x00FCu, 0x00FDu, 0x00FEu,\n    0x00FFu, 0x0102u, 0x0103u, 0x01A0u, 0x01A1u, 0x01AFu, 0x01B0u, 0x0110u, 0x0111u, 0x1EA2u,\n    0x1EA0u, 0x1EA3u, 0x1EA1u, 0x1EB0u, 0x1EAEu, 0x1EB2u, 0x1EB4u, 0x1EB6u, 0x1EB1u, 0x1EAFu,\n    0x1EB3u, 0x1EB5u, 0x1EB7u, 0x1EA6u, 0x1EA4u, 0x1EA8u, 0x1EAAu, 0x1EACu, 0x1EA7u, 0x1EA5u,\n    0x1EA9u, 0x1EABu, 0x1EADu, 0x1EBAu, 0x1EBCu, 0x1EB8u, 0x1EBBu, 0x1EBDu, 0x1EB9u, 0x1EC0u,\n    0x1EBEu, 0x1EC2u, 0x1EC4u, 0x1EC6u, 0x1EC1u, 0x1EBFu, 0x1EC3u, 0x1EC5u, 0x1EC7u, 0x1EC8u,\n    0x0128u, 0x1ECAu, 0x1EC9u, 0x0129u, 0x1ECBu, 0x1ECEu, 0x1ECCu, 0x1ECFu, 0x1ECDu, 0x1ED2u,\n    0x1ED0u, 0x1ED4u, 0x1ED6u, 0x1ED8u, 0x1ED3u, 0x1ED1u, 0x1ED5u, 0x1ED7u, 0x1ED9u, 0x1EDCu,\n    0x1EDAu, 0x1EDEu, 0x1EE0u, 0x1EE2u, 0x1EDDu, 0x1EDBu, 0x1EDFu, 0x1EE1u, 0x1EE3u, 0x1EE6u,\n    0x0168u, 0x1EE4u, 0x1EE7u, 0x0169u, 0x1EE5u, 0x1EEAu, 0x1EE8u, 0x1EECu, 0x1EEEu, 0x1EF0u,\n    0x1EEBu, 0x1EE9u, 0x1EEDu, 0x1EEFu, 0x1EF1u, 0x1EF2u, 0x1EF6u, 0x1EF8u, 0x1EF4u, 0x1EF3u,\n    0x1EF7u, 0x1EF9u, 0x1EF5u, 0x0141u, 0x0142u, 0x0152u, 0x0153u, 0x0160u, 0x0161u, 0x017Du,\n    0x017Eu, 0x0106u, 0x0107u, 0x010Cu, 0x010Du, 0x0158u, 0x0159u, 0x015Au, 0x015Bu, 0x0179u,\n    0x017Au, 0x017Bu, 0x017Cu, 0x2022u, 0x2661u, 0x2665u, 0x2606u, 0x2605u, 0x25C7u, 0x25C6u,\n    0x265Bu, 0x265Au, 0x2713u, 0x2726u, 0x2727u, 0x30C4u, 0x30E1u, 0x4E42u, 0x5F61u\n};\nstatic const uint8_t kSCBDRoyalAdvanceV058C[kSCBDRoyalGlyphCountV058C] = {\n    20, 24, 27, 31, 32, 52, 50, 20, 22, 22, 23, 34, 20, 32, 22, 22,\n    35, 21, 29, 26, 30, 27, 34, 25, 34, 33, 23, 20, 41, 31, 42, 30,\n    47, 44, 40, 48, 50, 37, 36, 49, 53, 24, 22, 47, 44, 60, 52, 49,\n    37, 48, 45, 35, 47, 50, 46, 61, 53, 47, 44, 25, 22, 25, 27, 26,\n    27, 31, 36, 29, 35, 29, 21, 35, 35, 20, 20, 36, 20, 51, 36, 36,\n    36, 36, 26, 28, 24, 36, 33, 50, 35, 31, 27, 25, 22, 25, 28, 20,\n    25, 30, 33, 31, 45, 22, 27, 28, 38, 22, 37, 35, 20, 26, 20, 22,\n    34, 21, 22, 33, 36, 49, 20, 20, 22, 25, 37, 44, 47, 45, 30, 27,\n    27, 27, 51, 51, 51, 66, 27, 27, 44, 27, 44, 29, 29, 29, 29, 52,\n    53, 53, 53, 53, 53, 53, 39, 53, 50, 50, 50, 50, 47, 44, 48, 41,\n    27, 41, 41, 41, 41, 58, 37, 39, 39, 39, 39, 26, 26, 26, 26, 42,\n    45, 42, 42, 42, 42, 42, 39, 27, 45, 45, 45, 27, 40, 44, 40, 51,\n    41, 56, 46, 57, 52, 52, 44, 51, 51, 41, 41, 51, 51, 51, 51, 51,\n    41, 41, 41, 41, 41, 51, 51, 51, 51, 51, 41, 41, 41, 41, 41, 44,\n    44, 44, 39, 39, 39, 44, 44, 44, 44, 44, 39, 39, 39, 39, 39, 29,\n    29, 29, 26, 26, 26, 53, 53, 42, 42, 53, 53, 53, 53, 53, 42, 42,\n    42, 42, 42, 56, 56, 56, 56, 56, 46, 46, 46, 46, 46, 50, 50, 50,\n    45, 45, 45, 57, 57, 57, 57, 57, 52, 52, 52, 52, 52, 47, 47, 47,\n    47, 40, 40, 40, 40, 45, 26, 67, 62, 40, 34, 45, 37, 45, 37, 45,\n    37, 48, 36, 40, 34, 45, 37, 45, 37, 29, 50, 50, 68, 64, 73, 73,\n    66, 66, 55, 58, 58, 66, 66, 66, 66\n};\n\nstatic const uint8_t kSCBDTimerAdvanceV058C[12] = {\n    59, 35, 49, 44, 50, 45, 58, 41, 57, 56, 36, 46\n};\n\nstatic Draw::Texture *GetSCBDRoyalUnicodeAtlasV058C(UIContext *ctx) {\n    if (!g_scbdRoyalUnicodeAtlasV058C && !g_scbdRoyalUnicodeAtlasV058CAttempted) {\n        g_scbdRoyalUnicodeAtlasV058CAttempted = true;\n        g_scbdRoyalUnicodeAtlasV058C = CreateTextureFromFile(\n            ctx->GetDrawContext(),\n            "scbd/winner_asset_v058c/royal_unicode_atlas.png",\n            ImageFileType::PNG,\n            false,\n            2048,\n            2048\n        );\n    }\n    return g_scbdRoyalUnicodeAtlasV058C;\n}\n\nstatic Draw::Texture *GetSCBDTimerAtlasV058C(UIContext *ctx) {\n    if (!g_scbdTimerAtlasV058C && !g_scbdTimerAtlasV058CAttempted) {\n        g_scbdTimerAtlasV058CAttempted = true;\n        g_scbdTimerAtlasV058C = CreateTextureFromFile(\n            ctx->GetDrawContext(),\n            "scbd/winner_asset_v058c/timer_digits.png",\n            ImageFileType::PNG,\n            false,\n            2048,\n            512\n        );\n    }\n    return g_scbdTimerAtlasV058C;\n}\n\nstatic const char *SCBDDecodeUTF8V058C(const char *p, uint32_t &cp) {\n    const unsigned char c0 = static_cast<unsigned char>(*p);\n    if (!c0) {\n        cp = 0;\n        return p;\n    }\n    if (c0 < 0x80) {\n        cp = c0;\n        return p + 1;\n    }\n\n    const unsigned char c1 = static_cast<unsigned char>(p[1]);\n    if (!c1) {\n        cp = static_cast<uint32_t>(\'?\');\n        return p + 1;\n    }\n    if ((c0 & 0xE0) == 0xC0) {\n        cp = ((c0 & 0x1F) << 6) | (c1 & 0x3F);\n        return p + 2;\n    }\n\n    const unsigned char c2 = static_cast<unsigned char>(p[2]);\n    if (!c2) {\n        cp = static_cast<uint32_t>(\'?\');\n        return p + 1;\n    }\n    if ((c0 & 0xF0) == 0xE0) {\n        cp = ((c0 & 0x0F) << 12) | ((c1 & 0x3F) << 6) | (c2 & 0x3F);\n        return p + 3;\n    }\n\n    const unsigned char c3 = static_cast<unsigned char>(p[3]);\n    if (!c3) {\n        cp = static_cast<uint32_t>(\'?\');\n        return p + 1;\n    }\n    if ((c0 & 0xF8) == 0xF0) {\n        cp = ((c0 & 0x07) << 18) | ((c1 & 0x3F) << 12) | ((c2 & 0x3F) << 6) | (c3 & 0x3F);\n        return p + 4;\n    }\n\n    cp = static_cast<uint32_t>(\'?\');\n    return p + 1;\n}\n\nstatic int SCBDRoyalGlyphIndexV058C(uint32_t cp) {\n    for (int i = 0; i < kSCBDRoyalGlyphCountV058C; ++i) {\n        if (kSCBDRoyalCodepointsV058C[i] == cp)\n            return i;\n    }\n    // Preferred visible fallback, then question mark.\n    for (int i = 0; i < kSCBDRoyalGlyphCountV058C; ++i) {\n        if (kSCBDRoyalCodepointsV058C[i] == 0x25C7u)\n            return i;\n    }\n    for (int i = 0; i < kSCBDRoyalGlyphCountV058C; ++i) {\n        if (kSCBDRoyalCodepointsV058C[i] == static_cast<uint32_t>(\'?\'))\n            return i;\n    }\n    return 0;\n}\n\nstatic float SCBDRoyalMeasureV058C(const char *text) {\n    if (!text)\n        return 0.0f;\n    float w = 0.0f;\n    const char *p = text;\n    while (*p) {\n        uint32_t cp = 0;\n        p = SCBDDecodeUTF8V058C(p, cp);\n        const int idx = SCBDRoyalGlyphIndexV058C(cp);\n        w += static_cast<float>(kSCBDRoyalAdvanceV058C[idx]);\n    }\n    return w;\n}\n\nstatic void DrawSCBDRoyalTextV058C(\n    UIContext *ctx,\n    const char *text,\n    float x,\n    float y,\n    float targetH,\n    float maxW,\n    int align\n) {\n    Draw::Texture *atlas = GetSCBDRoyalUnicodeAtlasV058C(ctx);\n    if (!atlas || !text || !*text)\n        return;\n\n    const float naturalW = SCBDRoyalMeasureV058C(text);\n    float scale = targetH / static_cast<float>(kSCBDRoyalCellHV058C);\n    float totalW = naturalW * scale;\n    if (maxW > 1.0f && totalW > maxW) {\n        scale *= maxW / totalW;\n        totalW = maxW;\n    }\n\n    float penX = x;\n    if (align == 1)\n        penX -= totalW * 0.5f;\n    else if (align == 2)\n        penX -= totalW;\n\n    const float drawW = static_cast<float>(kSCBDRoyalCellWV058C) * scale;\n    const float drawH = static_cast<float>(kSCBDRoyalCellHV058C) * scale;\n    const float topY = y - drawH * 0.5f;\n\n    ctx->Flush();\n    ctx->Begin();\n    ctx->GetDrawContext()->BindTexture(0, atlas);\n\n    const char *p = text;\n    while (*p) {\n        uint32_t cp = 0;\n        p = SCBDDecodeUTF8V058C(p, cp);\n        const int idx = SCBDRoyalGlyphIndexV058C(cp);\n        const int col = idx % kSCBDRoyalColsV058C;\n        const int row = idx / kSCBDRoyalColsV058C;\n        const float u1 = static_cast<float>(col * kSCBDRoyalCellWV058C) / static_cast<float>(kSCBDRoyalAtlasWV058C);\n        const float v1 = static_cast<float>(row * kSCBDRoyalCellHV058C) / static_cast<float>(kSCBDRoyalAtlasHV058C);\n        const float u2 = static_cast<float>((col + 1) * kSCBDRoyalCellWV058C) / static_cast<float>(kSCBDRoyalAtlasWV058C);\n        const float v2 = static_cast<float>((row + 1) * kSCBDRoyalCellHV058C) / static_cast<float>(kSCBDRoyalAtlasHV058C);\n        ctx->Draw()->DrawTexRect(\n            penX, topY,\n            penX + drawW, topY + drawH,\n            u1, v1, u2, v2,\n            0xFFFFFFFF\n        );\n        penX += static_cast<float>(kSCBDRoyalAdvanceV058C[idx]) * scale;\n    }\n\n    ctx->Flush();\n    ctx->RebindTexture();\n    ctx->BindFontTexture();\n}\n\nstatic int SCBDTimerGlyphIndexV058C(char c) {\n    if (c >= \'0\' && c <= \'9\')\n        return c - \'0\';\n    if (c == \'.\')\n        return 10;\n    return 11;  // s / fallback\n}\n\nstatic void DrawSCBDTimerV058C(\n    UIContext *ctx,\n    float cx,\n    float cy,\n    int remainingMs,\n    float maxW\n) {\n    Draw::Texture *atlas = GetSCBDTimerAtlasV058C(ctx);\n    if (!atlas)\n        return;\n\n    const int tenths = std::max(0, remainingMs / 100);\n    char timer[32];\n    std::snprintf(timer, sizeof(timer), "%d.%ds", tenths / 10, tenths % 10);\n\n    const int pulsePeriod = remainingMs <= 3000 ? 320 : remainingMs <= 5000 ? 520 : 900;\n    const int phase = pulsePeriod > 0 ? (remainingMs % pulsePeriod) : 0;\n    const int half = std::max(1, pulsePeriod / 2);\n    const float tri = phase <= half ? static_cast<float>(phase) / half :\n        static_cast<float>(pulsePeriod - phase) / half;\n    const float pulseAmp = remainingMs <= 3000 ? 0.11f : remainingMs <= 5000 ? 0.065f : 0.025f;\n    const float targetH = 76.0f * (1.0f + pulseAmp * tri);\n\n    float naturalW = 0.0f;\n    for (const char *p = timer; *p; ++p)\n        naturalW += static_cast<float>(kSCBDTimerAdvanceV058C[SCBDTimerGlyphIndexV058C(*p)]);\n\n    float scale = targetH / 148.0f;\n    float totalW = naturalW * scale;\n    if (maxW > 1.0f && totalW > maxW) {\n        scale *= maxW / totalW;\n        totalW = maxW;\n    }\n\n    float penX = cx - totalW * 0.5f;\n    const float drawW = 120.0f * scale;\n    const float drawH = 148.0f * scale;\n    const float topY = cy - drawH * 0.5f;\n\n    ctx->Flush();\n    ctx->Begin();\n    ctx->GetDrawContext()->BindTexture(0, atlas);\n    for (const char *p = timer; *p; ++p) {\n        const int idx = SCBDTimerGlyphIndexV058C(*p);\n        const float u1 = static_cast<float>(idx) / 12.0f;\n        const float u2 = static_cast<float>(idx + 1) / 12.0f;\n        ctx->Draw()->DrawTexRect(\n            penX, topY,\n            penX + drawW, topY + drawH,\n            u1, 0.0f, u2, 1.0f,\n            0xFFFFFFFF\n        );\n        penX += static_cast<float>(kSCBDTimerAdvanceV058C[idx]) * scale;\n    }\n    ctx->Flush();\n    ctx->RebindTexture();\n    ctx->BindFontTexture();\n}\n\n\nstatic std::string SCBDFormatNumberV058C(int value) {\n    std::string out = std::to_string(std::max(0, value));\n    for (int i = static_cast<int>(out.size()) - 3; i > 0; i -= 3)\n        out.insert(static_cast<size_t>(i), ",");\n    return out;\n}\n\nstatic void DrawSCBDRoyalFirstGlyphV058C(\n    UIContext *ctx,\n    const std::string &text,\n    float x,\n    float y,\n    float targetH\n) {\n    if (text.empty()) {\n        DrawSCBDRoyalTextV058C(ctx, "?", x, y, targetH, targetH * 1.2f, 1);\n        return;\n    }\n    const unsigned char c0 = static_cast<unsigned char>(text[0]);\n    int n = 1;\n    if ((c0 & 0xE0) == 0xC0) n = 2;\n    else if ((c0 & 0xF0) == 0xE0) n = 3;\n    else if ((c0 & 0xF8) == 0xF0) n = 4;\n    n = std::min(n, static_cast<int>(text.size()));\n    char buf[8] = {0};\n    for (int i = 0; i < n; ++i)\n        buf[i] = text[static_cast<size_t>(i)];\n    DrawSCBDRoyalTextV058C(ctx, buf, x, y, targetH, targetH * 1.2f, 1);\n}\n\n'
s = replace_once(
    s,
    "static void DrawSCBDTransparentTop5List(\n",
    royal_helper + "\nstatic void DrawSCBDTransparentTop5List(\n",
    "insert V0.5.8C Royal Unicode engine",
)

top5 = 'static void DrawSCBDTransparentTop5List(\n    UIContext *ctx,\n    FontID font,\n    const SCBDMatchMockRow rows[SCBD_TOP5_LIMIT],\n    float x,\n    float y,\n    float rowH,\n    float avatarSize,\n    float fontScale\n) {\n    (void)font;\n    const float rankW = 34.0f;\n    const float avatarX = x + rankW + avatarSize * 0.5f;\n    const float nameX = x + rankW + avatarSize + 10.0f;\n\n    ctx->Flush();\n    ctx->BeginNoTex();\n    for (int i = 0; i < SCBD_TOP5_LIMIT; ++i) {\n        const float cy = y + rowH * i + rowH * 0.5f;\n        const float radius = avatarSize * 0.5f;\n        ctx->Draw()->FillCircle(avatarX, cy, radius + 2.0f, 28, 0xC0000000);\n        ctx->Draw()->FillCircle(avatarX, cy, radius, 28, rows[i].avatarColor);\n    }\n    ctx->Flush();\n\n    const float textH = std::max(16.0f, std::min(25.0f, 46.0f * fontScale));\n    for (int i = 0; i < SCBD_TOP5_LIMIT; ++i) {\n        const float cy = y + rowH * i + rowH * 0.5f;\n        char rankText[8];\n        std::snprintf(rankText, sizeof(rankText), "#%d", i + 1);\n\n        DrawSCBDRoyalTextV058C(ctx, rankText, x, cy, textH, rankW - 2.0f, 0);\n        DrawSCBDRoyalTextV058C(ctx, rows[i].name, nameX, cy, textH, 150.0f, 0);\n        DrawSCBDRoyalTextV058C(ctx, rows[i].avatarText, avatarX, cy, textH * 0.80f, avatarSize * 0.70f, 1);\n    }\n\n    ctx->Flush();\n    ctx->RebindTexture();\n}\n\n'
s = replace_between(
    s,
    "static void DrawSCBDTransparentTop5List(\n",
    "static void DrawSCBDMatchTop5HUD(\n",
    top5,
    "replace Top5 text with Royal texture font",
)

rank_avatar = 'static void DrawSCBDRankAvatar(\n    UIContext *ctx,\n    FontID font,\n    const SCBDRankAvatarMock &user,\n    float cx,\n    float cy,\n    float radius,\n    int rank,\n    bool showTierFrame\n) {\n    (void)font;\n    ctx->Flush();\n    ctx->BeginNoTex();\n    ctx->Draw()->FillCircle(cx, cy, radius + 1.0f, 32, 0xD0101218);\n    ctx->Draw()->FillCircle(cx, cy, radius, 32, user.color);\n    ctx->Flush();\n\n    if (showTierFrame)\n        DrawSCBDRankFrame(ctx, rank, cx, cy, radius);\n\n    DrawSCBDRoyalTextV058C(ctx, user.initial, cx, cy, radius * 1.18f, radius * 1.45f, 1);\n}\n'
s = replace_between(
    s,
    "static void DrawSCBDRankAvatar(\n",
    "static Draw::Texture *g_scbdCharacterPortraitAtlas = nullptr;\n",
    rank_avatar,
    "replace ranking avatar initials with Royal texture font without deleting ranking atlas loader",
)

rank_block = '    if (page == Panel::RANK) {\n        static const char *tabs[4] = {"TOP TUAN","TOP THANG","TOP NHAN VAT","CHUOI WIN"};\n        const int active = RankTab();\n        for (int i = 0; i < 4; ++i) {\n            const Rect tr = RankTabRect(i, sw, sh);\n            DrawSCBDLayerButton(ctx, font, tr, "", i == active ? 0xEE9B7427 : 0xCC2A3240);\n            DrawSCBDRoyalTextV058C(\n                ctx, tabs[i],\n                tr.x + tr.w * 0.5f,\n                tr.y + tr.h * 0.5f,\n                17.0f,\n                tr.w - 12.0f,\n                1\n            );\n        }\n\n        const Rect list = RankListRect(sw, sh);\n        const float rowH = 36.0f;\n        const float scroll = RankScroll();\n        const int total = RankRowCount();\n        const int first = std::max(0, static_cast<int>(scroll / rowH));\n        const float yoff = -(scroll - first * rowH);\n        static const char *chars[28] = {\n            "ALGOL","AMY","ASTAROTH","CASSANDRA","CERVANTES","DAMPIERRE","HILDE",\n            "IVY","KILIK","KRATOS","LIZARDMAN","MAXI","MITSURUGI","NIGHTMARE",\n            "RAPHAEL","ROCK","SEONG_MI_NA","SETSUKA","SIEGFRIED","SOPHITIA","TAKI",\n            "TALIM","TIRA","VOLDO","XIANGHUA","YOSHIMITSU","YUN_SEONG","ZASALAMEL"\n        };\n\n        ctx->Flush();\n        ctx->BeginNoTex();\n        ctx->Draw()->Rect(list.x, list.y, list.w, list.h, 0xB810141C);\n        ctx->Flush();\n\n        for (int i = first; i < total; ++i) {\n            const float y = list.y + yoff + (i - first) * rowH;\n            if (y > list.y + list.h - 2.0f)\n                break;\n            if (y + rowH < list.y)\n                continue;\n\n            const float cy = y + rowH * 0.5f;\n            const uint32_t rowColor = (i % 2) ? 0x8C1D2430 : 0xA8252C38;\n            ctx->Flush();\n            ctx->BeginNoTex();\n            ctx->Draw()->Rect(list.x + 3.0f, y + 1.0f, list.w - 6.0f, rowH - 2.0f, rowColor);\n            ctx->Flush();\n\n            char rankText[12];\n            std::snprintf(rankText, sizeof(rankText), "%d", i + 1);\n            DrawSCBDRoyalTextV058C(ctx, rankText, list.x + 10.0f, cy, active == 2 ? 20.0f : 18.0f, 32.0f, 0);\n\n            if (active == 2) {\n                const float portraitX = list.x + 43.0f;\n                const float portraitW = 62.0f;\n                const float portraitH = rowH - 1.0f;\n\n                // IMPORTANT: this global ranking atlas is the original C4R1\n                // name-ordered atlas. It is never replaced by the auto-pick atlas.\n                DrawSCBDCharacterPortraitSlot(ctx, font, chars[i], i, portraitX, y + 0.5f, portraitW, portraitH);\n\n                DrawSCBDRoyalTextV058C(\n                    ctx,\n                    chars[i],\n                    portraitX + portraitW + 12.0f,\n                    cy,\n                    16.5f,\n                    145.0f,\n                    0\n                );\n\n                const float usersStart = list.x + std::min(292.0f, list.w * 0.36f);\n                const float userColumnW = (list.x + list.w - usersStart - 8.0f) / 3.0f;\n                for (int slot = 0; slot < 3; ++slot) {\n                    const int userIndex = (i + slot * 3) % 10;\n                    const SCBDRankAvatarMock &user = kSCBDRankUsers[userIndex];\n                    const float colX = usersStart + userColumnW * slot;\n                    const float avatarX = colX + 15.0f;\n                    DrawSCBDRankAvatar(ctx, font, user, avatarX, cy, 10.5f, slot + 1, true);\n                    DrawSCBDRoyalTextV058C(\n                        ctx,\n                        user.name,\n                        colX + 34.0f,\n                        cy,\n                        14.5f,\n                        userColumnW - 37.0f,\n                        0\n                    );\n                }\n            } else {\n                const SCBDRankAvatarMock &user = kSCBDRankUsers[i % 10];\n                const float avatarX = list.x + 58.0f;\n                DrawSCBDRankAvatar(ctx, font, user, avatarX, cy, 11.0f, i + 1, active != 3);\n\n                DrawSCBDRoyalTextV058C(\n                    ctx,\n                    user.name,\n                    list.x + 78.0f,\n                    cy,\n                    16.0f,\n                    list.w * 0.52f,\n                    0\n                );\n\n                std::string valueText;\n                if (active == 3) {\n                    const int best = std::max(1, 100 - i);\n                    valueText = std::to_string(best) + " WIN";\n                } else {\n                    const int base = active == 0 ? 1820000 : 9850000;\n                    const int step = active == 0 ? 9250 : 37850;\n                    valueText = SCBDFormatNumberV058C(std::max(1, base - i * step));\n                }\n                DrawSCBDRoyalTextV058C(\n                    ctx,\n                    valueText.c_str(),\n                    list.x + list.w - 14.0f,\n                    cy,\n                    16.5f,\n                    170.0f,\n                    2\n                );\n            }\n        }\n    }\n\n'
s = replace_between(
    s,
    "    if (page == Panel::RANK) {\n",
    "    if (page == Panel::DEV) {\n",
    rank_block,
    "replace ranking panel text/layout V0.5.8C",
)

old_title = '    ctx->Draw()->DrawText(font, title, panel.x + panel.w * 0.5f, panel.y + 30, 0xFFFFFFFF, ALIGN_CENTER | FLAG_DYNAMIC_ASCII);\n'
new_title = """    if (page == Panel::RANK) {
        DrawSCBDRoyalTextV058C(
            ctx, title,
            panel.x + panel.w * 0.5f,
            panel.y + 30.0f,
            27.0f,
            panel.w * 0.62f,
            1
        );
    } else {
        ctx->Draw()->DrawText(
            font, title,
            panel.x + panel.w * 0.5f,
            panel.y + 30,
            0xFFFFFFFF,
            ALIGN_CENTER | FLAG_DYNAMIC_ASCII
        );
    }
"""
s = replace_once(s, old_title, new_title, "replace ranking title font")

winner_renderer = '// WINNER FINAL V0.5.8C | Royal Unicode + exact auto-pick + ranking-safe atlas split\n\nstatic Draw::Texture *g_scbdWinnerFinalTextures[4] = {nullptr, nullptr, nullptr, nullptr};\nstatic bool g_scbdWinnerFinalTextureAttempted[4] = {false, false, false, false};\nstatic Draw::Texture *g_scbdWinnerKratosSplash = nullptr;\nstatic bool g_scbdWinnerKratosSplashAttempted = false;\nstatic Draw::Texture *g_scbdWinnerPickAtlasV058C = nullptr;\nstatic bool g_scbdWinnerPickAtlasV058CAttempted = false;\n\nstatic Draw::Texture *GetSCBDWinnerFinalTexture(UIContext *ctx, int index) {\n    static const char *paths[4] = {\n        "scbd/winner_asset_v057c4r1/victory_final.png",\n        "scbd/winner_asset_v057c4r1/pick_final.png",\n        "scbd/winner_asset_v057c4r1/locked_final.png",\n        "scbd/winner_asset_v057c4r1/timeout_final.png",\n    };\n    index = std::clamp(index, 0, 3);\n    if (!g_scbdWinnerFinalTextures[index] && !g_scbdWinnerFinalTextureAttempted[index]) {\n        g_scbdWinnerFinalTextureAttempted[index] = true;\n        g_scbdWinnerFinalTextures[index] = CreateTextureFromFile(\n            ctx->GetDrawContext(),\n            paths[index],\n            ImageFileType::PNG,\n            false,\n            2048,\n            1024\n        );\n    }\n    return g_scbdWinnerFinalTextures[index];\n}\n\nstatic Draw::Texture *GetSCBDWinnerPickAtlasV058C(UIContext *ctx) {\n    if (!g_scbdWinnerPickAtlasV058C && !g_scbdWinnerPickAtlasV058CAttempted) {\n        g_scbdWinnerPickAtlasV058CAttempted = true;\n        g_scbdWinnerPickAtlasV058C = CreateTextureFromFile(\n            ctx->GetDrawContext(),\n            "scbd/winner_asset_v058c/pick_portraits_exact.png",\n            ImageFileType::PNG,\n            false,\n            1024,\n            1024\n        );\n    }\n    return g_scbdWinnerPickAtlasV058C;\n}\n\nstatic Draw::Texture *GetSCBDWinnerKratosSplash(UIContext *ctx) {\n    if (!g_scbdWinnerKratosSplash && !g_scbdWinnerKratosSplashAttempted) {\n        g_scbdWinnerKratosSplashAttempted = true;\n        g_scbdWinnerKratosSplash = CreateTextureFromFile(\n            ctx->GetDrawContext(),\n            "scbd/winner_asset_v057c4r1/splash_10_kratos.png",\n            ImageFileType::PNG,\n            false,\n            1024,\n            1024\n        );\n    }\n    return g_scbdWinnerKratosSplash;\n}\n\nstatic void DrawSCBDFinalTexture(UIContext *ctx, const Bounds &bounds, int index) {\n    Draw::Texture *tex = GetSCBDWinnerFinalTexture(ctx, index);\n    if (!tex)\n        return;\n    ctx->Flush();\n    ctx->Begin();\n    ctx->GetDrawContext()->BindTexture(0, tex);\n    ctx->Draw()->DrawTexRect(\n        bounds.x, bounds.y,\n        bounds.x + bounds.w, bounds.y + bounds.h,\n        0.0f, 0.0f, 1.0f, 1.0f,\n        0xFFFFFFFF\n    );\n    ctx->Flush();\n    ctx->RebindTexture();\n    ctx->BindFontTexture();\n}\n\nstatic void DrawSCBDFinalText(\n    UIContext *ctx,\n    FontID font,\n    const char *text,\n    float x,\n    float y,\n    float scale,\n    uint32_t color,\n    int align\n) {\n    (void)font;\n    (void)color;\n    int royalAlign = 0;\n    if ((align & ALIGN_RIGHT) != 0)\n        royalAlign = 2;\n    else if ((align & ALIGN_HCENTER) != 0 || (align & ALIGN_CENTER) != 0)\n        royalAlign = 1;\n    const float targetH = std::max(10.0f, scale * 90.0f);\n    const float maxW = targetH * 11.5f;\n    DrawSCBDRoyalTextV058C(ctx, text, x, y, targetH, maxW, royalAlign);\n}\n\nstatic std::string SCBDFinalScore(int value) {\n    std::string out = std::to_string(std::max(0, value));\n    for (int i = static_cast<int>(out.size()) - 3; i > 0; i -= 3)\n        out.insert(static_cast<size_t>(i), ",");\n    return out;\n}\n\nstatic void DrawSCBDFinalAtlasPortrait(\n    UIContext *ctx,\n    int index,\n    float x,\n    float y,\n    float w,\n    float h\n) {\n    Draw::Texture *atlas = GetSCBDWinnerPickAtlasV058C(ctx);\n    if (!atlas)\n        return;\n    constexpr int kCols = 7;\n    constexpr int kRows = 4;\n    const int safeIndex = std::clamp(index, 0, 27);\n    const int col = safeIndex % kCols;\n    const int row = safeIndex / kCols;\n    const float u1 = static_cast<float>(col) / static_cast<float>(kCols);\n    const float v1 = static_cast<float>(row) / static_cast<float>(kRows);\n    const float u2 = static_cast<float>(col + 1) / static_cast<float>(kCols);\n    const float v2 = static_cast<float>(row + 1) / static_cast<float>(kRows);\n    ctx->Flush();\n    ctx->Begin();\n    ctx->GetDrawContext()->BindTexture(0, atlas);\n    ctx->Draw()->DrawTexRect(x, y, x + w, y + h, u1, v1, u2, v2, 0xFFFFFFFF);\n    ctx->Flush();\n    ctx->RebindTexture();\n    ctx->BindFontTexture();\n}\n\nstatic void DrawSCBDFinalKratosSplash(\n    UIContext *ctx,\n    float x,\n    float y,\n    float w,\n    float h\n) {\n    Draw::Texture *tex = GetSCBDWinnerKratosSplash(ctx);\n    if (!tex)\n        return;\n    ctx->Flush();\n    ctx->Begin();\n    ctx->GetDrawContext()->BindTexture(0, tex);\n    ctx->Draw()->DrawTexRect(x, y, x + w, y + h, 0.0f, 0.0f, 1.0f, 1.0f, 0xFFFFFFFF);\n    ctx->Flush();\n    ctx->RebindTexture();\n    ctx->BindFontTexture();\n}\n\nstatic void DrawSCBDFinalRoster(\n    UIContext *ctx,\n    FontID font,\n    const Bounds &bounds,\n    bool locked,\n    int selectedId\n) {\n    const float sx = bounds.w / 1280.0f;\n    const float sy = bounds.h / 720.0f;\n    auto X = [&](float v) { return bounds.x + v * sx; };\n    auto Y = [&](float v) { return bounds.y + v * sy; };\n    auto W = [&](float v) { return v * sx; };\n    auto H = [&](float v) { return v * sy; };\n\n    // Coordinates match the final approved production canvases.\n    const float startX = locked ? 343.0f : 246.0f;\n    const float startY1 = locked ? 487.0f : 478.0f;\n    const float startY2 = locked ? 529.0f : 533.0f;\n    const float stepX = locked ? 45.5f : 56.0f;\n    const float tileW = locked ? 34.0f : 43.0f;\n    const float tileH = locked ? 31.0f : 38.0f;\n\n    for (int i = 0; i < 28; ++i) {\n        const int col = i % 14;\n        const int row = i / 14;\n        const float px = startX + col * stepX;\n        const float py = row == 0 ? startY1 : startY2;\n\n        DrawSCBDFinalAtlasPortrait(ctx, i, X(px), Y(py), W(tileW), H(tileH));\n\n        // V0.5.7C4: visible slot number makes /pick 1-28 unambiguous.\n        ctx->Flush();\n        ctx->BeginNoTex();\n        ctx->Draw()->Rect(X(px), Y(py + tileH - 10.0f), W(tileW), H(10.0f), 0xD0181008);\n        ctx->Flush();\n        ctx->Begin();\n        ctx->BindFontTexture();\n        char slotNumber[8];\n        std::snprintf(slotNumber, sizeof(slotNumber), "%d", i + 1);\n        DrawSCBDFinalText(\n            ctx, font, slotNumber,\n            X(px + tileW * 0.5f), Y(py + tileH - 5.0f),\n            (0.18f * std::min(sx, sy)), 0xFFFFE7A8, ALIGN_CENTER\n        );\n\n        if (selectedId == i + 1) {\n            ctx->Flush();\n            ctx->BeginNoTex();\n            ctx->Draw()->Rect(\n                X(px - 2.0f), Y(py - 2.0f),\n                W(tileW + 4.0f), H(tileH + 4.0f),\n                0x88FFD34A\n            );\n            ctx->Flush();\n            ctx->Begin();\n            ctx->BindFontTexture();\n        }\n    }\n}\n\nstatic void DrawSCBDFinalAvatar(\n    UIContext *ctx,\n    FontID font,\n    float cx,\n    float cy,\n    float radius,\n    const std::string &username,\n    int team\n) {\n    (void)font;\n    (void)team;\n\n    // HOTFIX2: production PNG already owns the circular green avatar plate.\n    // Do not paint a second FillCircle on top of it.\n    DrawSCBDRoyalFirstGlyphV058C(ctx, username, cx, cy, radius * 1.18f);\n}\n\nstatic void DrawSCBDFinalCountdown(\n    UIContext *ctx,\n    FontID font,\n    float cx,\n    float cy,\n    int remainingMs\n) {\n    (void)font;\n    DrawSCBDTimerV058C(ctx, cx, cy, remainingMs, 185.0f);\n}\n\nstatic void DrawSCBDNativeWinnerLayer(UIContext *ctx, FontID font, const Bounds &bounds) {\n    const SCBDNativeWinner::Snapshot s = SCBDNativeWinner::Read();\n    if (s.phase == SCBDNativeWinner::Phase::NONE)\n        return;\n\n    const float sx = bounds.w / 1280.0f;\n    const float sy = bounds.h / 720.0f;\n    auto X = [&](float v) { return bounds.x + v * sx; };\n    auto Y = [&](float v) { return bounds.y + v * sy; };\n    auto W = [&](float v) { return v * sx; };\n    auto H = [&](float v) { return v * sy; };\n    auto S = [&](float v) { return v * std::min(sx, sy); };\n\n    const uint32_t teamAccent = s.team == 2 ? 0xFFFFA2B0 : 0xFFA0FFAE;\n\n    // Do not blur or cover the Top5 side areas. Only a light center dim is used.\n    ctx->Flush();\n    ctx->BeginNoTex();\n    ctx->Draw()->Rect(X(165.0f), bounds.y, W(950.0f), bounds.h, 0x30000000);\n    ctx->Flush();\n\n    if (s.phase == SCBDNativeWinner::Phase::WINNER) {\n        DrawSCBDFinalTexture(ctx, bounds, 0);\n\n        char victory[64];\n        std::snprintf(victory, sizeof(victory), "P%d VICTORY", s.team);\n        DrawSCBDFinalText(ctx, font, victory, X(640.0f), Y(316.0f), S(0.72f), 0xFFFFE6A1, ALIGN_CENTER);\n        DrawSCBDFinalText(ctx, font, "TOP 1 WINNER", X(640.0f), Y(365.0f), S(0.31f), 0xFFFFF0C2, ALIGN_CENTER);\n\n        DrawSCBDFinalAvatar(ctx, font, X(544.0f), Y(451.0f), S(36.0f), s.username, s.team);\n        char user[160];\n        std::snprintf(user, sizeof(user), "@%s", s.username.c_str());\n        DrawSCBDFinalText(ctx, font, user, X(746.0f), Y(460.0f), S(0.40f), 0xFFFFEDB2, ALIGN_CENTER);\n    } else if (s.phase == SCBDNativeWinner::Phase::PICK) {\n        DrawSCBDFinalTexture(ctx, bounds, 1);\n\n        DrawSCBDFinalAvatar(ctx, font, X(275.0f), Y(371.0f), S(38.0f), s.username, s.team);\n\n        char user[160];\n        std::snprintf(user, sizeof(user), "@%s", s.username.c_str());\n        DrawSCBDFinalText(ctx, font, user, X(473.0f), Y(333.0f), S(0.34f), 0xFFFFEFC3, ALIGN_CENTER);\n\n        char team[64];\n        std::snprintf(team, sizeof(team), "TEAM P%d", s.team);\n        DrawSCBDFinalText(ctx, font, team, X(473.0f), Y(374.0f), S(0.30f), teamAccent, ALIGN_CENTER);\n\n        const std::string score = std::string("SCORE ") + SCBDFinalScore(s.score);\n        DrawSCBDFinalText(ctx, font, score.c_str(), X(473.0f), Y(413.0f), S(0.28f), 0xFFFFDEA0, ALIGN_CENTER);\n\n        DrawSCBDFinalCountdown(ctx, font, X(1005.0f), Y(362.0f), s.remainingMs);\n        DrawSCBDFinalRoster(ctx, font, bounds, false, 0);\n    } else if (s.phase == SCBDNativeWinner::Phase::PICK_SUCCESS) {\n        DrawSCBDFinalTexture(ctx, bounds, 2);\n\n        const int atlasIndex = std::clamp(s.characterId - 1, 0, 27);\n        if (s.characterId == 14 || s.character == "KRATOS") {\n            DrawSCBDFinalKratosSplash(ctx, X(414.0f), Y(277.0f), W(208.0f), H(235.0f));\n        } else {\n            // Splash hook: non-Kratos characters currently fall back to the live atlas\n            // until their dedicated splash assets are added.\n            DrawSCBDFinalAtlasPortrait(ctx, atlasIndex, X(447.0f), Y(305.0f), W(138.0f), H(155.0f));\n        }\n\n        // HOTFIX2 Locked In clean dynamic fields.\n        // Cover only stale baked VALUE areas. Keep the gold borders and labels.\n        ctx->Flush();\n        ctx->BeginNoTex();\n        ctx->Draw()->Rect(X(691.0f), Y(319.0f), W(232.0f), H(31.0f), 0xF00A2118);\n        ctx->Draw()->Rect(X(704.0f), Y(386.0f), W(204.0f), H(24.0f), 0xF00A2118);\n        ctx->Draw()->Rect(X(804.0f), Y(422.0f), W(112.0f), H(31.0f), 0xF00A2118);\n        ctx->Flush();\n\n        // Character name in the upper value panel.\n        DrawSCBDRoyalTextV058C(\n            ctx,\n            s.character.c_str(),\n            X(807.0f),\n            Y(335.0f),\n            S(s.character.size() > 12 ? 23.0f : 27.0f),\n            W(214.0f),\n            1\n        );\n\n        // Winner username below the baked PICKED BY label.\n        char picked[180];\n        std::snprintf(picked, sizeof(picked), "@%s", s.username.c_str());\n        DrawSCBDRoyalTextV058C(\n            ctx,\n            picked,\n            X(807.0f),\n            Y(399.0f),\n            S(s.username.size() > 14 ? 18.0f : 21.0f),\n            W(186.0f),\n            1\n        );\n\n        // Team value stays in the right-hand box and no longer covers TEAM.\n        char team[64];\n        std::snprintf(team, sizeof(team), "P%d", s.team);\n        DrawSCBDRoyalTextV058C(\n            ctx,\n            team,\n            X(860.0f),\n            Y(438.0f),\n            S(22.0f),\n            W(86.0f),\n            1\n        );\n\n        DrawSCBDFinalRoster(ctx, font, bounds, true, s.characterId);\n    } else if (s.phase == SCBDNativeWinner::Phase::TIMEOUT) {\n        // Pure visual notice. Soulcalibur/existing controller remains the random owner.\n        DrawSCBDFinalTexture(ctx, bounds, 3);\n    }\n\n    ctx->Draw()->SetFontScale(1.0f, 1.0f);\n    ctx->Flush();\n    ctx->RebindTexture();\n}\n'
s = replace_between(
    s,
    "static Draw::Texture *g_scbdWinnerFinalTextures[4]",
    "static void DrawSCBDBoneMapper(",
    winner_renderer,
    "replace C4R1 winner renderer with V0.5.8C Royal Unicode renderer",
)

debug.write_text(s, encoding="utf-8")

final = debug.read_text(encoding="utf-8")
for marker in (
    "WINNER FINAL V0.5.8C",
    "V0.5.8C Royal Unicode / Numeral Texture Engine",
    "winner_asset_v058c/pick_portraits_exact.png",
    "winner_asset_v058c/royal_unicode_atlas.png",
    "winner_asset_v058c/timer_digits.png",
    "GetSCBDWinnerPickAtlasV058C",
    "DrawSCBDRoyalTextV058C",
    "DrawSCBDTimerV058C",
):
    if marker not in final:
        raise SystemExit(f"V0.5.8C generated source missing: {marker}")

a = final.index("// WINNER FINAL V0.5.8C")
b = final.index("static void DrawSCBDBoneMapper(", a)
winner_section = final[a:b]
if "GetSCBDCharacterPortraitAtlas(ctx)" in winner_section:
    raise SystemExit("V0.5.8C safety failure: Winner still uses ranking portrait atlas")
if 's.characterId == 14 || s.character == "KRATOS"' not in winner_section:
    raise SystemExit("V0.5.8C safety failure: Kratos auto-pick ID 14 marker missing")
if "std::clamp(s.characterId - 1, 0, 27)" not in winner_section:
    raise SystemExit("V0.5.8C safety failure: Locked-In is not using auto-pick ID directly")

rank_a = final.index("    if (page == Panel::RANK) {")
rank_b = final.index("    if (page == Panel::DEV) {", rank_a)
rank_section = final[rank_a:rank_b]
if "DrawSCBDCharacterPortraitSlot(ctx, font, chars[i], i" not in rank_section:
    raise SystemExit("V0.5.8C safety failure: Ranking name->portrait mapping changed")
if "pick_portraits_exact" in rank_section:
    raise SystemExit("V0.5.8C safety failure: auto-pick atlas leaked into ranking")

# HOTFIX1 compile-safety: V0.5.8C must preserve the V0.5.3/C4R1 ranking atlas loader.
if "static Draw::Texture *GetSCBDCharacterPortraitAtlas(UIContext *ctx)" not in final:
    raise SystemExit("V0.5.8C HOTFIX1 safety failure: ranking atlas loader was deleted")
if "GetSCBDCharacterPortraitAtlas(ctx)" not in final:
    raise SystemExit("V0.5.8C HOTFIX1 safety failure: ranking portrait renderer lost its atlas call")

with info.open("a", encoding="utf-8") as f:
    f.write(
        "\nPSP Live FloGB V0.5.8C Royal Unicode + Portrait Mapping Fix\n"
        "Base: V0.5.7C4R1 proven clean build lane\n"
        "Winner/Top5/Ranking dynamic text uses custom texture font, not default PPSSPP DrawText\n"
        "UTF-8 Vietnamese + Latin Extended + common symbol fallback atlas\n"
        "Dedicated large timer numeral atlas with pulse\n"
        "Ranking atlas restored to original C4R1 name order\n"
        "Auto-pick 1-28 uses a separate atlas; custom and Random excluded\n"
        "Kratos auto-pick id = 14; ranking KRATOS row remains independent\n"
    )


# HOTFIX3 source-safety checks: ignore comments, detect only real FillCircle calls.
if "HOTFIX2 Locked In clean dynamic fields" not in final:
    raise SystemExit("V0.5.8C HOTFIX2 safety failure: Locked In fix missing")
if "DrawSCBDFinalAvatar(ctx, font, X(544.0f), Y(451.0f)" not in final:
    raise SystemExit("V0.5.8C HOTFIX2 safety failure: Victory avatar center missing")
if "DrawSCBDFinalAvatar(ctx, font, X(275.0f), Y(371.0f)" not in final:
    raise SystemExit("V0.5.8C HOTFIX2 safety failure: Pick avatar center missing")

avatar_a = final.index("static void DrawSCBDFinalAvatar(")
avatar_b = final.index("static void DrawSCBDFinalCountdown(", avatar_a)
avatar_section = final[avatar_a:avatar_b]
if "ctx->Draw()->FillCircle(" in avatar_section:
    raise SystemExit("V0.5.8C HOTFIX3 safety failure: avatar renderer still paints an extra circle")


# -----------------------------------------------------------------------------
# HOTFIX4 / V0.5.8D POLISH LAYER
# -----------------------------------------------------------------------------
v058d = debug.read_text(encoding="utf-8")

def _v058d_between(text, start, end, replacement, label):
    a = text.find(start)
    if a < 0:
        raise SystemExit(f"V0.5.8D {label}: start marker missing")
    b = text.find(end, a + len(start))
    if b < 0:
        raise SystemExit(f"V0.5.8D {label}: end marker missing")
    return text[:a] + replacement + "\n\n" + text[b:]

def _v058d_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"V0.5.8D {label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)

_v058d_glyph_index = r'''static int SCBDRoyalGlyphIndexV058C(uint32_t cp) {
    if (cp >= 0x0300u && cp <= 0x036Fu)
        return -1;

    for (int i = 0; i < kSCBDRoyalGlyphCountV058C; ++i) {
        if (kSCBDRoyalCodepointsV058C[i] == cp)
            return i;
    }
    for (int i = 0; i < kSCBDRoyalGlyphCountV058C; ++i) {
        if (kSCBDRoyalCodepointsV058C[i] == 0x25C7u)
            return i;
    }
    for (int i = 0; i < kSCBDRoyalGlyphCountV058C; ++i) {
        if (kSCBDRoyalCodepointsV058C[i] == static_cast<uint32_t>('?'))
            return i;
    }
    return 0;
}'''

v058d = _v058d_between(
    v058d,
    "static int SCBDRoyalGlyphIndexV058C(uint32_t cp) {",
    "static float SCBDRoyalMeasureV058C(",
    _v058d_glyph_index,
    "glyph fallback",
)

_v058d_measure = r'''static float SCBDRoyalMeasureV058C(const char *text) {
    if (!text)
        return 0.0f;

    constexpr float kTracking = 1.35f;
    float w = 0.0f;
    int visible = 0;
    const char *p = text;
    while (*p) {
        uint32_t cp = 0;
        p = SCBDDecodeUTF8V058C(p, cp);
        const int idx = SCBDRoyalGlyphIndexV058C(cp);
        if (idx < 0)
            continue;
        if (visible > 0)
            w += kTracking;
        w += static_cast<float>(kSCBDRoyalAdvanceV058C[idx]);
        ++visible;
    }
    return w;
}'''

v058d = _v058d_between(
    v058d,
    "static float SCBDRoyalMeasureV058C(",
    "static void DrawSCBDRoyalTextV058C(",
    _v058d_measure,
    "Royal text measurement",
)

_v058d_royal_text = r'''static void DrawSCBDRoyalTextV058C(
    UIContext *ctx,
    const char *text,
    float x,
    float y,
    float targetH,
    float maxW,
    int align
) {
    Draw::Texture *atlas = GetSCBDRoyalUnicodeAtlasV058C(ctx);
    if (!atlas || !text || !*text)
        return;

    constexpr float kTracking = 1.35f;
    const float naturalW = SCBDRoyalMeasureV058C(text);
    float scale = targetH / static_cast<float>(kSCBDRoyalCellHV058C);
    float totalW = naturalW * scale;
    if (maxW > 1.0f && totalW > maxW) {
        scale *= maxW / totalW;
        totalW = maxW;
    }

    float penX = x;
    if (align == 1)
        penX -= totalW * 0.5f;
    else if (align == 2)
        penX -= totalW;

    const float drawW = static_cast<float>(kSCBDRoyalCellWV058C) * scale;
    const float drawH = static_cast<float>(kSCBDRoyalCellHV058C) * scale;
    const float topY = y - drawH * 0.5f;

    ctx->Flush();
    ctx->Begin();
    ctx->GetDrawContext()->BindTexture(0, atlas);

    const char *p = text;
    bool firstVisible = true;
    while (*p) {
        uint32_t cp = 0;
        p = SCBDDecodeUTF8V058C(p, cp);
        const int idx = SCBDRoyalGlyphIndexV058C(cp);
        if (idx < 0)
            continue;

        if (!firstVisible)
            penX += kTracking * scale;
        firstVisible = false;

        const int col = idx % kSCBDRoyalColsV058C;
        const int row = idx / kSCBDRoyalColsV058C;
        const float inset = 0.75f;
        const float u1 = static_cast<float>(col * kSCBDRoyalCellWV058C + inset) / static_cast<float>(kSCBDRoyalAtlasWV058C);
        const float v1 = static_cast<float>(row * kSCBDRoyalCellHV058C + inset) / static_cast<float>(kSCBDRoyalAtlasHV058C);
        const float u2 = static_cast<float>((col + 1) * kSCBDRoyalCellWV058C - inset) / static_cast<float>(kSCBDRoyalAtlasWV058C);
        const float v2 = static_cast<float>((row + 1) * kSCBDRoyalCellHV058C - inset) / static_cast<float>(kSCBDRoyalAtlasHV058C);

        const float advancePx = static_cast<float>(kSCBDRoyalAdvanceV058C[idx]) * scale;
        const float cellPad = (static_cast<float>(kSCBDRoyalCellWV058C) * scale - advancePx) * 0.5f;
        const float glyphX = penX - cellPad;

        ctx->Draw()->DrawTexRect(
            glyphX, topY,
            glyphX + drawW, topY + drawH,
            u1, v1, u2, v2,
            0xFFFFFFFF
        );
        penX += advancePx;
    }

    ctx->Flush();
    ctx->RebindTexture();
    ctx->BindFontTexture();
}'''

v058d = _v058d_between(
    v058d,
    "static void DrawSCBDRoyalTextV058C(",
    "static int SCBDTimerGlyphIndexV058C(",
    _v058d_royal_text,
    "Royal text renderer",
)

_v058d_timer = r'''static void DrawSCBDTimerV058C(
    UIContext *ctx,
    float cx,
    float cy,
    int remainingMs,
    float maxW
) {
    Draw::Texture *atlas = GetSCBDTimerAtlasV058C(ctx);
    if (!atlas)
        return;

    const int tenths = std::max(0, remainingMs / 100);
    char timer[32];
    std::snprintf(timer, sizeof(timer), "%d.%ds", tenths / 10, tenths % 10);

    const int pulsePeriod = remainingMs <= 3000 ? 320 : remainingMs <= 5000 ? 520 : 900;
    const int phase = pulsePeriod > 0 ? (remainingMs % pulsePeriod) : 0;
    const int half = std::max(1, pulsePeriod / 2);
    const float tri = phase <= half ? static_cast<float>(phase) / half :
        static_cast<float>(pulsePeriod - phase) / half;
    const float pulseAmp = remainingMs <= 3000 ? 0.11f : remainingMs <= 5000 ? 0.065f : 0.025f;
    const float targetH = 76.0f * (1.0f + pulseAmp * tri);

    float naturalW = 0.0f;
    for (const char *p = timer; *p; ++p)
        naturalW += static_cast<float>(kSCBDTimerAdvanceV058C[SCBDTimerGlyphIndexV058C(*p)]);

    float scale = targetH / 148.0f;
    float totalW = naturalW * scale;
    if (maxW > 1.0f && totalW > maxW) {
        scale *= maxW / totalW;
        totalW = maxW;
    }

    float penX = cx - totalW * 0.5f;
    const float drawW = 120.0f * scale;
    const float drawH = 148.0f * scale;
    const float topY = cy - drawH * 0.5f;

    ctx->Flush();
    ctx->Begin();
    ctx->GetDrawContext()->BindTexture(0, atlas);
    for (const char *p = timer; *p; ++p) {
        const int idx = SCBDTimerGlyphIndexV058C(*p);
        const float inset = 0.75f;
        const float u1 = (static_cast<float>(idx * 120) + inset) / 1440.0f;
        const float u2 = (static_cast<float>((idx + 1) * 120) - inset) / 1440.0f;
        ctx->Draw()->DrawTexRect(
            penX, topY,
            penX + drawW, topY + drawH,
            u1, inset / 148.0f, u2, (148.0f - inset) / 148.0f,
            0xFFFFFFFF
        );
        penX += static_cast<float>(kSCBDTimerAdvanceV058C[idx]) * scale;
    }

    ctx->Flush();
    ctx->RebindTexture();
    ctx->BindFontTexture();
}'''

v058d = _v058d_between(
    v058d,
    "static void DrawSCBDTimerV058C(",
    "static std::string SCBDFormatNumberV058C(",
    _v058d_timer,
    "timer renderer",
)

_v058d_roster = r'''static void DrawSCBDFinalRoster(
    UIContext *ctx,
    FontID font,
    const Bounds &bounds,
    bool locked,
    int selectedId,
    int pickSuccessElapsedMs
) {
    const float sx = bounds.w / 1280.0f;
    const float sy = bounds.h / 720.0f;
    auto X = [&](float v) { return bounds.x + v * sx; };
    auto Y = [&](float v) { return bounds.y + v * sy; };
    auto W = [&](float v) { return v * sx; };
    auto H = [&](float v) { return v * sy; };

    const float startX = locked ? 343.0f : 246.0f;
    const float startY1 = locked ? 487.0f : 478.0f;
    const float startY2 = locked ? 529.0f : 533.0f;
    const float stepX = locked ? 45.5f : 56.0f;
    const float tileW = locked ? 34.0f : 43.0f;
    const float tileH = locked ? 31.0f : 38.0f;

    for (int i = 0; i < 28; ++i) {
        const int col = i % 14;
        const int row = i / 14;
        const float baseX = startX + col * stepX;
        const float baseY = row == 0 ? startY1 : startY2;
        const bool selected = selectedId == i + 1;

        float pop = 1.0f;
        bool pulseOn = false;
        if (selected && pickSuccessElapsedMs >= 0 && pickSuccessElapsedMs < 1100) {
            const int cycle = pickSuccessElapsedMs % 300;
            const int half = 150;
            const float tri = cycle <= half ? static_cast<float>(cycle) / half :
                static_cast<float>(300 - cycle) / half;
            pop = 1.0f + 0.10f * tri;
            pulseOn = ((pickSuccessElapsedMs / 150) % 2) == 0;
        }

        const float drawW = tileW * pop;
        const float drawH = tileH * pop;
        const float px = baseX - (drawW - tileW) * 0.5f;
        const float py = baseY - (drawH - tileH) * 0.5f;

        DrawSCBDFinalAtlasPortrait(ctx, i, X(px), Y(py), W(drawW), H(drawH));

        ctx->Flush();
        ctx->BeginNoTex();
        ctx->Draw()->Rect(X(px), Y(py + drawH - 10.0f), W(drawW), H(10.0f), 0xD0181008);

        if (selected) {
            const float t = pulseOn ? 4.0f : 2.0f;
            const uint32_t c = pulseOn ? 0xFFFFD85Au : 0xFF29E69Au;
            ctx->Draw()->Rect(X(px - t), Y(py - t), W(drawW + t * 2.0f), H(t), c);
            ctx->Draw()->Rect(X(px - t), Y(py + drawH), W(drawW + t * 2.0f), H(t), c);
            ctx->Draw()->Rect(X(px - t), Y(py), W(t), H(drawH), c);
            ctx->Draw()->Rect(X(px + drawW), Y(py), W(t), H(drawH), c);
        }
        ctx->Flush();

        char slotNumber[8];
        std::snprintf(slotNumber, sizeof(slotNumber), "%d", i + 1);
        DrawSCBDFinalText(
            ctx, font, slotNumber,
            X(baseX + tileW * 0.5f), Y(baseY + tileH - 5.0f),
            (0.18f * std::min(sx, sy)), 0xFFFFE7A8, ALIGN_CENTER
        );
    }
}'''

v058d = _v058d_between(
    v058d,
    "static void DrawSCBDFinalRoster(",
    "static void DrawSCBDFinalAvatar(",
    _v058d_roster,
    "pick-success roster",
)

v058d = _v058d_once(
    v058d,
    "DrawSCBDFinalAvatar(ctx, font, X(544.0f), Y(451.0f), S(36.0f), s.username, s.team);",
    "DrawSCBDFinalAvatar(ctx, font, X(542.5f), Y(456.5f), S(35.0f), s.username, s.team);",
    "Victory avatar center",
)
v058d = _v058d_once(
    v058d,
    "DrawSCBDFinalAvatar(ctx, font, X(275.0f), Y(371.0f), S(38.0f), s.username, s.team);",
    "DrawSCBDFinalAvatar(ctx, font, X(275.0f), Y(369.3f), S(37.0f), s.username, s.team);",
    "Pick avatar center",
)

v058d = _v058d_once(
    v058d,
    "DrawSCBDFinalRoster(ctx, font, bounds, false, 0);",
    "DrawSCBDFinalRoster(ctx, font, bounds, false, 0, -1);",
    "Pick roster call",
)

_v058d_large = r'''        const int atlasIndex = std::clamp(s.characterId - 1, 0, 27);
        const int pickSuccessElapsedMs = std::clamp(4500 - s.remainingMs, 0, 4500);

        const float tRaw = std::min(1.0f, static_cast<float>(pickSuccessElapsedMs) / 700.0f);
        const float ease = tRaw * (2.0f - tRaw);
        float pop = 0.88f + 0.12f * ease;

        if (pickSuccessElapsedMs < 1100) {
            const int cycle = pickSuccessElapsedMs % 300;
            const int half = 150;
            const float tri = cycle <= half ? static_cast<float>(cycle) / half :
                static_cast<float>(300 - cycle) / half;
            pop *= 1.0f + 0.035f * tri;
        }

        const float portraitCX = 518.0f;
        const float portraitCY = 394.0f;
        const float portraitW = 208.0f * pop;
        const float portraitH = 208.0f * pop;
        const float portraitX = portraitCX - portraitW * 0.5f;
        const float portraitY = portraitCY - portraitH * 0.5f;

        if (s.characterId == 14 || s.character == "KRATOS") {
            DrawSCBDFinalKratosSplash(
                ctx,
                X(portraitX - 2.0f), Y(portraitY - 10.0f),
                W(portraitW + 4.0f), H(portraitH + 20.0f)
            );
        } else {
            DrawSCBDFinalAtlasPortrait(
                ctx,
                atlasIndex,
                X(portraitX), Y(portraitY),
                W(portraitW), H(portraitH)
            );
        }
'''

v058d = _v058d_between(
    v058d,
    "        const int atlasIndex = std::clamp(s.characterId - 1, 0, 27);",
    "        // HOTFIX2 Locked In clean dynamic fields.",
    _v058d_large,
    "dynamic Locked-In portrait",
)

v058d = _v058d_once(
    v058d,
    "DrawSCBDFinalRoster(ctx, font, bounds, true, s.characterId);",
    "DrawSCBDFinalRoster(ctx, font, bounds, true, s.characterId, pickSuccessElapsedMs);",
    "Locked roster call",
)

v058d = v058d.replace(
    "// WINNER FINAL V0.5.8C |",
    "// V0.5.8D PICK SUCCESS POLISH\n// WINNER FINAL V0.5.8C |",
    1,
)

debug.write_text(v058d, encoding="utf-8")

_v058d_final = debug.read_text(encoding="utf-8")
_v058d_required = (
    "V0.5.8D PICK SUCCESS POLISH",
    "cp >= 0x0300u && cp <= 0x036Fu",
    "const float inset = 0.75f;",
    "pickSuccessElapsedMs",
    "portraitCX = 518.0f",
    "DrawSCBDFinalAvatar(ctx, font, X(542.5f), Y(456.5f)",
    "DrawSCBDFinalAvatar(ctx, font, X(275.0f), Y(369.3f)",
)
_v058d_missing = [m for m in _v058d_required if m not in _v058d_final]
if _v058d_missing:
    raise SystemExit(f"V0.5.8D source safety failure: {_v058d_missing}")

with info.open("a", encoding="utf-8") as f:
    f.write(
        "\nPSP Live FloGB V0.5.8D Pick Success Polish\n"
        "Exact avatar center correction\n"
        "Royal glyph UV bleed/spacing correction\n"
        "Unicode combining-mark fallback\n"
        "Selected small portrait pulse/glow\n"
        "Dynamic large portrait from /pick characterId with pop animation\n"
        "Ranking mapping preserved\n"
    )

print("PSP Live FloGB V0.5.8C patch applied successfully.")
