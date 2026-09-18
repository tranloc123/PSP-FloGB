from pathlib import Path
from PIL import Image
import numpy as np
import sys

if len(sys.argv) != 3:
    raise SystemExit(
        "Usage: build_scbd_rank_frame_atlas_v054a.py "
        "<source_strip.jpg> <output_atlas.png>"
    )

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

img = Image.open(src).convert("RGB")
cols = 7
cell_size = 220
inner_size = 208
padding = (cell_size - inner_size) // 2
bounds = [round(i * img.width / cols) for i in range(cols + 1)]

atlas = Image.new("RGBA", (cell_size * cols, cell_size), (0, 0, 0, 0))

for i in range(cols):
    tile = img.crop((bounds[i], 0, bounds[i + 1], img.height)).convert("RGBA")
    arr = np.asarray(tile).copy().astype(np.float32)
    rgb = arr[..., :3]

    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    sat = mx - mn

    # Preserve all outer metallic corners better than V0.5.4.
    alpha = np.clip((mx - 12.0) * 3.8, 0.0, 255.0)
    alpha = np.maximum(alpha, np.clip((lum - 7.0) * 3.2, 0.0, 255.0))
    alpha = np.maximum(alpha, np.clip((sat - 14.0) * 4.0, 0.0, 255.0))

    h, w = alpha.shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx = w * 0.50
    cy = h * 0.50
    nx = (xx - cx) / (w * 0.40)
    ny = (yy - cy) / (h * 0.39)
    rr = np.sqrt(nx * nx + ny * ny)

    # Smaller, feathered center hole so it does not eat the corner ornaments.
    hole = 1.0 - np.clip((rr - 0.86) / 0.08, 0.0, 1.0)
    vertical_gate = np.clip((yy / h - 0.10) / 0.70, 0.0, 1.0) * np.clip((0.76 - yy / h) / 0.20, 0.0, 1.0)
    alpha *= (1.0 - hole * vertical_gate)

    # Very soft border fade only at the extreme image boundary.
    border = np.ones_like(alpha)
    fade = 4
    for x in range(fade):
        factor = x / fade
        border[:, x] *= factor
        border[:, -1 - x] *= factor
        border[x, :] *= factor
        border[-1 - x, :] *= factor
    alpha *= border

    arr[..., 3] = np.clip(alpha, 0.0, 255.0).astype(np.uint8)
    rgba = Image.fromarray(arr.astype("uint8"), "RGBA").resize((inner_size, inner_size), Image.Resampling.LANCZOS)

    cell = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))
    cell.alpha_composite(rgba, (padding, padding))
    atlas.alpha_composite(cell, (i * cell_size, 0))

dst.parent.mkdir(parents=True, exist_ok=True)
atlas.save(dst, optimize=True)

print(
    f"SCBD V0.5.4a tier-frame atlas created: {dst} "
    f"{atlas.width}x{atlas.height}, 7 tiers"
)
