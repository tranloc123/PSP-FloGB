# PSP Live FloGB V0.5.7C — Winner Asset Integration Pass 1

This build replaces the V0.5.7B code-painted approximation with the **approved production asset pack**.

## What changes
- The four approved 1280×720 RGBA assets are embedded directly in the patcher:
  - `victory_intro.png`
  - `pick_phase.png`
  - `locked_in.png`
  - `timeout.png`
- The native winner renderer now loads those PNGs directly.
- Dynamic data remains native and live:
  - P1/P2 winner
  - `@USERNAME`
  - team
  - score
  - countdown
  - selected character
  - picker
  - 28 character portraits
  - selected roster highlight
- The three user/group/trophy glyphs from the earlier Pick concept are removed from the production Pick asset.
- `TIME OUT → GAME RANDOM` is visual only. The APK still does **not** invent the random result.

## Preserved
- Input Core V1
- V0.5.7A winner timing/state machine
- Top5 battle HUD
- tracker/avatar backend
- V0.5.6 rank visuals
- Web Winner V5 fallback
- random ownership remains with Soulcalibur/existing random controller

## Upload to `main`
1. `tools/apply_psp_live_flogb_v0_5_7c.py`
2. `README_V0_5_7C.md`
3. `.github/workflows/build-psp-live-flogb-v0.5.7c.yml`

The four PNGs are embedded inside the patcher, so there are still only **3 GitHub files** to upload.

## Workflow
`Build PSP Live FloGB V0.5.7C Winner Asset Integration Pass 1`

It auto-runs when the V0.5.7C patcher or workflow file is pushed to `main`.

## Output
APK:
`PSP_Live_FloGB_V0_5_7C_Winner_Asset_Integration_Pass_1.apk`

Artifact:
`PSP-Live-FloGB-V0.5.7C-Winner-Asset-Integration-Pass-1-APK`

## Device test order
1. Full Flow P1 / TINA.
2. Pick Phase: check avatar, username, team, score, timer and 28 portraits align with the production asset.
3. Locked In: check the large selected portrait, character name, picker/team and slot 10 highlight.
4. Time Out: show the approved `TIME OUT / GAME RANDOM` art, then close.
5. Verify Soulcalibur, not the APK, still owns random selection.
6. Verify Input Core and Top5 HUD remain unchanged.

## Production asset SHA-256
- `victory_intro.png`: `0bddb06f3e02c5279ae2976da30e6480e62d3e62ac1502b10cddd3605ae19497`
- `pick_phase.png`: `fa96a1380d444ca0668435c08cb7714fe63ed582265f0d1577aa8c43d982a84c`
- `locked_in.png`: `4a90ce89376644401213f8cf6e5d244452c83fb67d63d057c8decea5a3c47056`
- `timeout.png`: `5a09f3fe0fb475c04307f4ad5b2430f359be1cf3c3fad2cbd63dad56d701c8e7`
