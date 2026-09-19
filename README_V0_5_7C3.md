# PSP Live FloGB V0.5.7C3 — Final Asset Integration

This build integrates the latest **balanced-avatar form** approved after V0.5.7C2 review.

## Visual changes
- Uses the newest four Royal Gold + Emerald production canvases.
- Victory is compact and centered.
- Pick Phase is balanced around avatar / live identity / `/pick 1-28` / timer.
- Locked In gives the character image more visual weight without swallowing the screen.
- Time Out remains the cleanest compact state.
- Top5 left/right safe areas stay outside the center dim.
- Pick/Locked roster use 28 live character portraits with gold selected-slot highlight.

## Dynamic fields
- P1/P2 victory
- @username
- team
- score
- 15-second countdown
- selected character name
- picker
- selected roster slot

## Locked In splash
- Slot 10 / KRATOS uses a dedicated large splash asset in this test build.
- The renderer contains a splash hook for the remaining characters.
- Until their dedicated splash pack is added, non-Kratos selections fall back to the existing character atlas.

## Preserved
- Input Core V1
- Winner state/timing logic
- `/pick 1-28`
- Top5 battle HUD
- avatar/tracker backend
- Web Winner fallback
- Soulcalibur/existing controller remains owner of Random selection

## Upload paths
Upload these 3 files to `main`:

1. `tools/apply_psp_live_flogb_v0_5_7c3.py`
2. `README_V0_5_7C3.md`
3. `.github/workflows/build-psp-live-flogb-v0.5.7c3.yml`

The PNG production assets are embedded in the patcher.

## Workflow
`Build PSP Live FloGB V0.5.7C3 Final Asset Integration`

## Output
APK:
`PSP_Live_FloGB_V0_5_7C3_Final_Asset_Integration.apk`

Artifact:
`PSP-Live-FloGB-V0.5.7C3-Final-Asset-Integration-APK`

## Test order
1. Full Flow P1 / TINA.
2. Pick Phase: inspect avatar balance, username/team/score, timer and all 28 slots.
3. Locked In: slot 10 KRATOS, verify dedicated larger splash and gold slot highlight.
4. Full Flow P2 / EHBUDDEN.
5. Timeout: verify only the visual TIME OUT / GAME RANDOM state, then game-owned Random.
6. Input Lab regression test.

## Embedded asset SHA-256
- `victory_final.png`: `4f948f1f1a05ef04147ee533436de22993f85e811bfa4867b5db74d331b5035f`
- `pick_final.png`: `081ac51c519453fd9afbb9b63a5422ee35305f3bdadd5917b65a8642a23abff0`
- `locked_final.png`: `b8f542a6d55d6c764badeda808402870ea07ec99c16727c795e06e72f0d013a1`
- `timeout_final.png`: `06ee2f20da5046b8ea69a2d33fb845850af0c0905be0c3a900ade7ef03ca2e7e`
- `splash_10_kratos.png`: `44701468dfed4c810cba594ebb7b4dbfcf755bc38237b35a3ac1d015b80b5860`
