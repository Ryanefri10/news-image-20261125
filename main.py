#!/usr/bin/env python3
"""Deliver the 25 November 2026 front page for make.fun news-image-20261125.

The entry image is a pre-rendered PNG vendored next to this script
(entry.png, 1024x1024). This program does no drawing: it reads the
vendored artwork, validates it chunk by chunk, and copies it into the
output directory the harness provides.

Run:  MAKEFUN_OUTPUT_DIR=<dir> python3 main.py
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTWORK = HERE / "entry.png"
OUTPUT_NAME = "entry.png"

# sha256 of the vendored front page, as rendered for 25 November 2026.
EXPECTED_SHA256 = "a915673ed866a7490f058533f848d323538c1dbf305bf7d31dde15ee65bf8f86"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # entry image must fit in 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_artwork(path):
    """Load the vendored PNG bytes, refusing anything too short to hold
    a header."""
    blob = path.read_bytes()
    if len(blob) < 33:
        raise ValueError(f"{path.name} is too short to be a PNG")
    return blob


def inspect_signature(blob):
    if blob[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: bad 8-byte signature")
    return blob


def inspect_header(blob):
    """Return (width, height) from the IHDR chunk that opens the file."""
    chunk_len = struct.unpack(">I", blob[8:12])[0]
    chunk_type = blob[12:16]
    if chunk_type != b"IHDR":
        raise ValueError(f"first chunk is {chunk_type!r}, expected IHDR")
    if chunk_len != 13:
        raise ValueError(f"IHDR length is {chunk_len}, expected 13")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"page is {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    bit_depth, colour_type = blob[24], blob[25]
    if bit_depth != 8 or colour_type != 2:
        raise ValueError(
            f"IHDR says bit depth {bit_depth}, colour type {colour_type}; "
            "expected 8-bit RGB (depth 8, type 2)"
        )
    return blob


def inspect_chunks(blob):
    """Walk every PNG chunk from IHDR to IEND, checking each length
    stays inside the file and each CRC matches its type + data."""
    import zlib

    offset = 8
    seen_iend = False
    while offset + 8 <= len(blob):
        length = struct.unpack(">I", blob[offset:offset + 4])[0]
        chunk_type = blob[offset + 4:offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        if data_end + 4 > len(blob):
            raise ValueError(
                f"chunk {chunk_type!r} at {offset} runs past the file"
            )
        stored_crc = struct.unpack(">I", blob[data_end:data_end + 4])[0]
        actual_crc = zlib.crc32(chunk_type + blob[data_start:data_end])
        if stored_crc != actual_crc:
            raise ValueError(
                f"chunk {chunk_type!r} at {offset} has a bad CRC"
            )
        if chunk_type == b"IEND":
            seen_iend = True
            if data_end + 4 != len(blob):
                raise ValueError("trailing bytes after IEND")
            break
        offset = data_end + 4
    if not seen_iend:
        raise ValueError("no IEND chunk found")
    return blob


def inspect_trailer(blob):
    """The file must end with a well-formed IEND chunk."""
    tail = blob[-12:]
    tail_len, tail_type = struct.unpack(">I", tail[:4])[0], tail[4:8]
    if tail_type != b"IEND" or tail_len != 0:
        raise ValueError("file does not end with an IEND chunk")
    return blob


def confirm_digest(blob):
    if len(blob) > MAX_BYTES:
        raise ValueError(
            f"artwork is {len(blob)} bytes, over the {MAX_BYTES} limit"
        )
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(
            f"artwork digest mismatch: got {digest}, "
            f"expected {EXPECTED_SHA256}"
        )
    return digest


def deliver_copy(blob, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    target.write_bytes(blob)
    return target


def output_dir():
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not raw:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    return Path(raw)


def main():
    blob = read_artwork(ARTWORK)
    blob = inspect_signature(blob)
    blob = inspect_header(blob)
    blob = inspect_chunks(blob)
    blob = inspect_trailer(blob)
    digest = confirm_digest(blob)
    target = deliver_copy(blob, output_dir())
    print(
        f"delivered {target} "
        f"({EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, sha256 {digest})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
