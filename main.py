#!/usr/bin/env python3
"""World news in one image -- Sunday 22 November 2026.

Entry program for make.fun competition news-image-20261122. The poster
the repository holds (poster.png.b64, a base64-encoded PNG) is decoded
and written to the grader's output directory as entry.png.

Pure Python standard library only. No network access. Deterministic:
every run writes the exact same bytes. Nothing is written into the
repository; the only write goes to $MAKEFUN_OUTPUT_DIR (or ./output).
"""

import base64
import hashlib
import os
import struct
import sys

ASSET_NAME = "poster.png.b64"
OUTPUT_NAME = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
# sha256 of the poster.png this asset encodes (rendered by build_poster.py).
EXPECTED_SHA256 = "7f91ee74edf7c0b2d03c86e7ed948fb12baa2a14f3b62f67f2958023dc73cc4c"


def repo_dir():
    """Directory holding this program (the repository root in the grader)."""
    return os.path.dirname(os.path.abspath(__file__))


def output_dir():
    """Grader output directory, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(os.getcwd(), "output")
    return out


def load_poster(path):
    """Decode the base64 poster asset and return its PNG bytes."""
    with open(path, "rb") as fh:
        encoded = fh.read()
    # The asset is one long base64 line; tolerate surrounding whitespace.
    raw = base64.b64decode(b"".join(encoded.split()), validate=True)
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError("decoded asset is not a PNG image")
    if len(raw) > MAX_BYTES:
        raise ValueError("decoded poster is over the 1 MiB limit")
    return raw


def check_dimensions(raw):
    """Read the PNG IHDR chunk and return (width, height).

    Raises ValueError unless the image is exactly the required size.
    """
    if len(raw) < 24 or raw[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk where one is expected")
    width, height = struct.unpack(">II", raw[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"poster is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return width, height


def main():
    asset = os.path.join(repo_dir(), ASSET_NAME)
    if not os.path.isfile(asset):
        print(f"error: poster asset not found: {asset}", file=sys.stderr)
        return 1
    try:
        png = load_poster(asset)
        width, height = check_dimensions(png)
    except (ValueError, base64.binascii.Error) as exc:
        print(f"error: poster asset is invalid: {exc}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(png).hexdigest()
    if digest != EXPECTED_SHA256:
        print(
            "error: poster bytes do not match the expected sha256 "
            f"(got {digest})",
            file=sys.stderr,
        )
        return 1

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, OUTPUT_NAME)
    with open(out_path, "wb") as fh:
        fh.write(png)

    print(
        f"wrote {out_path}: {len(png)} bytes, "
        f"{width}x{height}, sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
