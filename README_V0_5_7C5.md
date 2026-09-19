# PSP Live FloGB V0.5.7C5 — Clean Dynamic Layer Rebuild

This is a fresh build lane with NEW filenames. It does not reuse the failed C4 workflow.

## Two failures found and fixed

### 1. First C4 failure
The patcher received `ppsspp` as the repository root, then incorrectly appended another `ppsspp/`, so it searched for:

`ppsspp/ppsspp/UI/DebugOverlay.cpp`

R1 uses the correct root.

### 2. HOTFIX1 failure
HOTFIX1 applied successfully, but its workflow still used stale preflight checks from an older experimental renderer. The first marker passed, then the obsolete `GetSCBDWinnerC4Texture` check failed.

While re-auditing the renderer, one additional compile-time problem was also found before Gradle:
`DrawSCBDFinalRoster()` used an undefined `S()` helper. R1 fixes this too.

## R1 visual changes retained
- Victory avatar fit + warmer gold text
- Pick avatar fit
- username / team / score text polish
- larger centered countdown
- slot numbers 1–28 restored, row-major 1–14 / 15–28
- Locked In Kratos splash rebalanced
- character name / picker / team moved inside their panels
- Timeout unchanged
- Input Core / Top5 / Random ownership unchanged

## Fresh filenames
Upload these three files to `main`:

1. `tools/apply_psp_live_flogb_v0_5_7c4r1.py`
2. `README_V0_5_7C4R1.md`
3. `.github/workflows/build-psp-live-flogb-v0.5.7c4r1.yml`

The old C4 files can stay in the repo. This new workflow does not depend on them.

## Output
APK:
`PSP_Live_FloGB_V0_5_7C4R1_Clean_Dynamic_Layer_Rebuild.apk`

Artifact:
`PSP-Live-FloGB-V0.5.7C5-Clean-Dynamic-Layer-Rebuild-APK`


## C5 focus
- Re-tune avatar placement in Victory and Pick screens.
- Increase slot number readability for /pick 1-28 on phone and TikTok Studio.
- Add pulsing countdown text for the timer.
- Tighten Locked In splash and text alignment.
