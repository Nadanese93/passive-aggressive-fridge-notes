#!/usr/bin/env python3
"""Write the Notes From a Passive-Aggressive Fridge entry.

Deterministic, stdlib only: no network, no randomness, no clock.
Writes the entry text to ``entry.txt`` in the output directory given by
the ``MAKEFUN_OUTPUT_DIR`` environment variable (default /tmp/makefun-out).
"""

import hashlib
import os
import sys

ENTRY = "I replaced your shopping list with a list of everything you never ate. It is longer."

MAX_LENGTH = 200


class BlankError(ValueError):
    """Entry is empty or only whitespace."""


class LengthError(ValueError):
    """Entry exceeds the maximum character length."""


class MultiLineError(ValueError):
    """Entry contains more than one line."""


def validate(text):
    if not text or text.strip() == "":
        raise BlankError("entry must not be empty or only whitespace")
    if len(text) > MAX_LENGTH:
        raise LengthError("entry exceeds %d characters" % MAX_LENGTH)
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/tmp/makefun-out")
    validate(ENTRY)
    os.makedirs(out_dir, exist_ok=True)
    data = ENTRY.encode("utf-8")
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise IOError("read-back mismatch: entry.txt does not match entry")
    digest = hashlib.sha256(data).hexdigest()
    print("Wrote %s (%d bytes, sha256 %s)" % (path, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
