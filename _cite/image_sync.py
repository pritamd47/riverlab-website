#!/usr/bin/env python3
"""Auto-generate responsive image variants for images/."""

import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

IMAGES_DIR = Path("images")
SIZES = [72, 400, 800, 1200]
SKIP_EXTENSIONS = {".svg", ".gif", ".webp", ".ico"}
VARIANT_RE = re.compile(r"-\d+w$")


def is_variant(path: Path) -> bool:
    return bool(VARIANT_RE.search(path.stem))


def generate_variants(src: Path) -> int:
    if src.suffix.lower() in SKIP_EXTENSIONS or is_variant(src):
        return 0

    count = 0
    try:
        with Image.open(src) as img:
            original_width = img.width
            mode = img.mode
            for size in SIZES:
                if size >= original_width:
                    continue
                out = src.parent / f"{src.stem}-{size}w{src.suffix}"
                if out.exists():
                    continue
                ratio = size / original_width
                resized = img.resize(
                    (size, max(1, int(img.height * ratio))), Image.LANCZOS
                )
                save_kwargs: dict = {}
                if src.suffix.lower() in (".jpg", ".jpeg"):
                    if resized.mode in ("RGBA", "P"):
                        resized = resized.convert("RGB")
                    save_kwargs = {"quality": 85, "optimize": True}
                elif src.suffix.lower() == ".png":
                    save_kwargs = {"optimize": True}
                resized.save(out, **save_kwargs)
                print(f"  {out.name}")
                count += 1
    except Exception as e:
        print(f"  error processing {src.name}: {e}", file=sys.stderr)
    return count


def sync_all() -> None:
    print("Syncing image variants...")
    total = sum(
        generate_variants(p)
        for p in sorted(IMAGES_DIR.iterdir())
        if p.is_file() and not p.name.startswith(".")
    )
    print(f"Done — {total} variant(s) generated.")


if __name__ == "__main__":
    sync_all()
