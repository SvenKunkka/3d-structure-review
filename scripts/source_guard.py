#!/usr/bin/env python3
"""Record/verify input-file SHA-256 baselines; never overwrite a manifest."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def digest(path):
    before = path.stat()
    if not path.is_file():
        raise ValueError(f"Not a regular file: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError(f"File changed while reading: {path}")
    return {"path": str(path), "bytes": after.st_size,
            "mtime_ns": after.st_mtime_ns, "sha256": h.hexdigest()}


def snapshot(manifest, files):
    paths = list(dict.fromkeys(Path(f).expanduser().resolve(strict=True) for f in files))
    if manifest in paths:
        raise ValueError("Manifest cannot also be an input file")
    if manifest.exists():
        raise FileExistsError(f"Refusing to overwrite manifest: {manifest}")
    result = {"schema_version": 1,
              "recorded_at": datetime.now(timezone.utc).isoformat(),
              "purpose": "Input byte-integrity baseline, not CAD validation",
              "files": [digest(p) for p in paths]}
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return {"manifest": str(manifest), "recorded_files": len(paths)}, 0


def verify(manifest):
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("schema_version") != 1 or not saved.get("files"):
        raise ValueError("Expected a nonempty schema_version 1 source manifest")
    checks = []
    for original in saved["files"]:
        path = Path(original["path"])
        try:
            current = digest(path)
            same = (current["bytes"] == original["bytes"]
                    and current["sha256"] == original["sha256"])
            checks.append({"path": str(path), "status": "unchanged" if same else "changed",
                           "expected_sha256": original["sha256"],
                           "actual_sha256": current["sha256"]})
        except (OSError, ValueError) as error:
            checks.append({"path": str(path), "status": "unreadable", "error": str(error)})
    ok = all(row["status"] == "unchanged" for row in checks)
    return {"manifest": str(manifest), "all_unchanged": ok, "checks": checks}, 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    snap = modes.add_parser("snapshot", help="Create a new baseline; refuses overwrite")
    snap.add_argument("--manifest", type=Path, required=True)
    snap.add_argument("--files", nargs="+", required=True)
    check = modes.add_parser("verify", help="Compare files with the stored baseline")
    check.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = args.manifest.expanduser().resolve()
        result, status = (snapshot(manifest, args.files) if args.mode == "snapshot"
                          else verify(manifest))
    except (OSError, ValueError, KeyError, TypeError) as error:
        result, status = {"error": str(error)}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
