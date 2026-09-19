# PSP Live FloGB V0.5.7B — Winner Visual Polish Pass 1

**Art direction locked:** Style A — **Royal Gold Ceremony**.

## Base
- V0.5.7 Runtime Core / Input Core V1: preserved.
- V0.5.7A Native Winner Visual V2 logic: preserved.
- V0.5.6 ranking/HUD baseline: preserved.
- Web Winner V5 remains LIVE fallback.

## What changes in V0.5.7B
- Replaces the flat cyan/DEV-looking Winner presentation with an embedded **gold + bronze + emerald** Royal Gold Ceremony theme.
- Adds four embedded native UI assets directly from the patcher:
  - `winner_victory.png`
  - `winner_pick.png`
  - `winner_locked.png`
  - `winner_timeout.png`
- Victory Intro: large `P1/P2 VICTORY`, Top 1 reveal, royal frame/ribbon/crown styling.
- Pick Phase: winner identity, team, score, `/pick 1-28`, 15-second ring, 28-character grid.
- Locked In: selected character presentation, picker, team and selected-slot highlight.
- Timeout: **TIME OUT → GAME RANDOM** only. APK does **not** decide the random character.
- Bottom runtime diagnostic line is hidden in normal gameplay. Tracking/backend remains active.

## Upload paths
Upload these three files to `main`:

1. `tools/apply_psp_live_flogb_v0_5_7b.py`
2. `README_V0_5_7B.md`
3. `.github/workflows/build-psp-live-flogb-v0.5.7b.yml`

The Royal Gold Ceremony PNG assets are embedded inside the patcher, so **no separate image upload is required**.

## Workflow
`Build PSP Live FloGB V0.5.7B Winner Visual Polish Pass 1`

The workflow auto-starts when the V0.5.7B patcher or workflow file is pushed to `main`. It can also be started manually with **Run workflow**.

## Output APK
`PSP_Live_FloGB_V0_5_7B_Winner_Visual_Polish_Pass_1.apk`

Artifact:
`PSP-Live-FloGB-V0.5.7B-Winner-Visual-Polish-Pass-1-APK`

## Test order
1. `WINNER ROYAL V0.5.7B` → Full Flow P1 / TINA.
2. Full Flow P2 / EHBUDDEN.
3. Locked In → slot 10 / KRATOS.
4. Time Out → must show only `TIME OUT`, `?`, `GAME RANDOM`, then close.
5. Verify game/random controller still owns Random selection.
6. Verify Input Lab still controls P1 correctly.
7. Verify Top5 and ranking screens are unchanged.
8. Verify bottom native diagnostic line is no longer visible during normal play.

## Important
V0.5.7B is a **visual polish pass**, not a bridge cutover and not Dual Input P2. Do not change Input Core or Winner logic while validating this build.
