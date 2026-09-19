# PSP Live FloGB V0.5.7C4 — Dynamic Layer Polish Pass 1

This pass keeps the approved Royal Gold + Emerald production art direction and focuses on the **dynamic layer** so the overlay no longer feels like dev text pasted on top of the render.

## Main fixes
- Rebalanced **avatar placement** in Victory and Pick.
- Polished **dynamic text layout** for Victory / Pick / Locked In.
- Unified the dynamic typography tone with warmer gold / cream rendering.
- Re-centered the **pick countdown** so it sits better in the right timer emblem.
- Restored **slot numbers 1–28** on the character roster in Pick and Locked.
- Refined **Locked In** character presentation:
  - dedicated Kratos splash remains supported
  - splash moved and resized for better symmetry
  - character name / picker / team re-aligned into the right-side info panels
- Timeout kept visually stable because it was already the cleanest state.

## What this pass intentionally does NOT change
- Input Core V1
- Winner state logic
- `/pick 1-28`
- winner timing / timeout timing
- Top5 match HUD
- Web Winner fallback
- game-owned random selection after timeout

## Upload these 3 files to `main`
1. `tools/apply_psp_live_flogb_v0_5_7c4.py`
2. `README_V0_5_7C4.md`
3. `.github/workflows/build-psp-live-flogb-v0.5.7c4.yml`

## Workflow
`Build PSP Live FloGB V0.5.7C4 Dynamic Layer Polish Pass 1`

## Output APK
`PSP_Live_FloGB_V0_5_7C4_Dynamic_Layer_Polish_Pass_1.apk`

## Suggested test order
1. Victory screen: confirm avatar fit + `P1/P2 VICTORY` + `TOP 1 WINNER` + username alignment.
2. Pick Phase: confirm avatar fit, username/team/score readability, timer centering, and visible slot numbers 1–28.
3. Locked In: test `/pick 10` Kratos and verify splash balance, character name fit, picker field, team field, and highlighted slot.
4. Timeout: verify `TIME OUT / GAME RANDOM` visual remains clean.
5. Regression: full flow on both Team P1 and Team P2.

## Embedded asset SHA-256
- `victory_final.png`: `4f948f1f1a05ef04147ee533436de22993f85e811bfa4867b5db74d331b5035f`
- `pick_final.png`: `37082f695787f88425b1a49803d049359dee6f2422c65fd2dab962dbe15bcf0f`
- `locked_final.png`: `38af3dc6d3b5e1be1c170b3e5c235c08b29c6db2add6ce558ebaf537edbb1738`
- `timeout_final.png`: `06ee2f20da5046b8ea69a2d33fb845850af0c0905be0c3a900ade7ef03ca2e7e`
- `splash_10_kratos.png`: `bf174bf49995bd3a7605548618fa95c2ba736b8553e38899f276e6548bda4e46`
