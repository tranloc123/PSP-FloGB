# PSP Live FloGB V0.5.7C4 HOTFIX1

## Why the first C4 build failed
The workflow correctly called:

`python3 tools/apply_psp_live_flogb_v0_5_7c4.py ppsspp`

but the patcher treated that argument as the workspace root and appended `ppsspp/` again, so it looked for:

`ppsspp/ppsspp/UI/DebugOverlay.cpp`

This hotfix uses the argument as the PPSSPP repo root and correctly opens:

`UI/DebugOverlay.cpp`

## Visual changes kept
- larger/better-fitted avatar in Victory and Pick
- warmer gold/cream dynamic text
- larger centered countdown
- slot numbers 1–28 restored
- Locked In Kratos splash repositioned/resized
- character name / picker / team moved into their correct panels
- Timeout remains unchanged

## Upload
Replace the same three files on `main`:
1. `tools/apply_psp_live_flogb_v0_5_7c4.py`
2. `README_V0_5_7C4.md`
3. `.github/workflows/build-psp-live-flogb-v0.5.7c4.yml`

The corrected patcher/workflow push will trigger a new build automatically.
