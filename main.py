#!/usr/bin/env python3
"""Sum up 23 November 2026's world news in one image.

The entry image (news-2026-11-23-v2.png, a classic newspaper-style
1024x1024 front page with 39 dated stories, drawn by
draw_v2_20261123.py for this bounty) is stored in this repository.
This program hands it to the grader: it copies the image to the
output directory as entry.png, using only the Python standard
library so it runs anywhere.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
The image is a PNG of 1024x1024 pixels, well under the 1 MiB limit.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news-2026-11-23-v2.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
