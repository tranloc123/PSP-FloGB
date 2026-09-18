# PSP Live FloGB V0.5.7A - Native Winner Visual V2

Baseline: V0.5.7 Runtime Core + Native Winner V1.

## Scope

V0.5.7A only upgrades the native Winner/Pick presentation. The V0.5.7 Input Core V1 and the V0.5.6 HUD/ranking visuals are intentionally frozen.

## Winner V2 flow

1. WINNER INTRO (2.2s)
   - P1 VICTORY / P2 VICTORY
   - TOP 1 WINNER reveal
   - Top1 avatar/username reveal
   - cinematic darkened background + team color/gold sweep

2. PICK PHASE (15s)
   - Top1 winner card
   - username, team, score
   - /pick 1-28
   - segmented countdown indicator
   - full 28-character native portrait grid

3. PICK SUCCESS
   - LOCKED IN
   - large selected-character portrait
   - selected slot highlighted in the 28-character grid
   - picker username + team
   - DEV test uses KRATOS at correct atlas slot 10

4. TIMEOUT
   - TIME OUT
   - ?
   - GAME RANDOM
   - then native layer closes
   - IMPORTANT: APK does NOT select a random character and does NOT display a fabricated random result. Soulcalibur / the existing Random selection controller owns the random result.

## DEV Winner V2 Lab

- TEST FULL FLOW - P1 / TINA
- TEST FULL FLOW - P2 / EHBUDDEN
- TEST LOCKED IN - 10 KRATOS
- TEST TIME OUT - GAME RANDOM
- CANCEL NATIVE WINNER

## Unchanged / protected

- V0.5.7 native Input Core V1
- TAP / CHORD / SEQUENCE input route
- V0.5.6 Top5 battle HUD
- Week/Month/Character/Win ranking screens
- rank frames / character portrait atlas
- fighter avatar tracking
- legacy green memory inspector remains hidden
- Web Winner V5 remains live fallback; Live Bridge cutover is not part of V0.5.7A

## Build

GitHub Actions:

`Build PSP Live FloGB V0.5.7A Native Winner Visual V2`

Artifact:

`PSP-Live-FloGB-V0.5.7A-Native-Winner-Visual-V2-APK`

APK:

`PSP_Live_FloGB_V0_5_7A_Native_Winner_Visual_V2.apk`

## Test order

1. Confirm current Top5 HUD is unchanged.
2. Confirm INPUT LAB still controls P1 exactly as V0.5.7.
3. SCBD -> WINNER V2 LAB -> TEST FULL FLOW P1.
4. Confirm P1 VICTORY intro transitions to 15s pick phase.
5. Confirm 28 portrait grid is visible and readable.
6. Test LOCKED IN 10 KRATOS.
7. Test TIME OUT. It must show GAME RANDOM only and MUST NOT show a character result.
8. Repeat full flow for P2.
