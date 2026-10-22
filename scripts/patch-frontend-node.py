#!/usr/bin/env python3
"""Apply the reviewed Node-only patch to the pinned upstream Dockerfile."""

import hashlib
from pathlib import Path
import sys


EXPECTED_SHA256 = "59bd67473118a261cf896f8af3e8495de4a01f6667f11456f559647cd76736ac"
OLD_IMAGE = "node:22.14.0-alpine"
NEW_IMAGE = "node:22.23.4-alpine"
EXPECTED_STAGES = [
    f"FROM {OLD_IMAGE} AS deps",
    f"FROM {OLD_IMAGE} AS builder",
    f"FROM {OLD_IMAGE} AS runner",
]


def patched_dockerfile(original: bytes) -> bytes:
    if hashlib.sha256(original).hexdigest() != EXPECTED_SHA256:
        raise ValueError("upstream Dockerfile changed; review the security patch again")
    text = original.decode("utf-8")
    stages = [line for line in text.splitlines() if line.upper().startswith("FROM ")]
    if stages != EXPECTED_STAGES or text.count(OLD_IMAGE) != len(EXPECTED_STAGES):
        raise ValueError("unexpected Node base stages; refusing a partial patch")
    for stage in EXPECTED_STAGES:
        text = text.replace(stage, stage.replace(OLD_IMAGE, NEW_IMAGE), 1)
    if OLD_IMAGE in text or text.count(NEW_IMAGE) != len(EXPECTED_STAGES):
        raise ValueError("Node patch verification failed")
    return text.encode("utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: patch-frontend-node.py <upstream Dockerfile>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        original = path.read_bytes()
        patched = patched_dockerfile(original)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Node security patch refused: {error}", file=sys.stderr)
        return 1
    path.write_bytes(patched)
    print(f"Patched all three frontend stages to {NEW_IMAGE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
