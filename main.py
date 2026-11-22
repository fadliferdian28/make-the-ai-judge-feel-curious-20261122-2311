"""Copy entry.txt into the output directory and prove the copy is exact.

The grader sets MAKEFUN_OUTPUT_DIR; when it is absent we fall back to
/output. Only the standard library is used, and nothing is written
anywhere except the output directory.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def digest(path):
    """Return the SHA-256 hex digest of a file's bytes."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def check_text(path):
    """Read the entry and confirm it passes the gate: 1-280 code points,
    and not only whitespace. Returns the code-point count."""
    text = path.read_text(encoding="utf-8")
    count = len(text)
    if count < 1 or count > 280:
        raise ValueError(f"entry is {count} code points, outside 1-280")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    return count


def main():
    source = Path(__file__).resolve().parent / "entry.txt"
    try:
        char_count = check_text(source)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"error: entry failed the gate: {exc}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"

    if target.resolve() == source.resolve():
        print("error: output path is the source file itself", file=sys.stderr)
        return 1

    try:
        shutil.copyfile(source, target)
    except shutil.SameFileError:
        print("error: source and destination are the same file", file=sys.stderr)
        return 1

    source_hash = digest(source)
    target_hash = digest(target)
    if source_hash != target_hash:
        print("error: copy does not match source", file=sys.stderr)
        return 1

    print(f"verified: entry.txt ({char_count} chars) copied to {target} (sha256 {target_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
