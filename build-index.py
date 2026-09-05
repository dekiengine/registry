#!/usr/bin/env python3
"""Generate index.json from packages/*.json.

index.json is the catalogue the editor fetches first; packages/<id>.json is what
it fetches for a package's version list (DekiRegistrySource::FetchVersions).
They used to be maintained by hand in parallel and had already drifted --
deki-gps and deki-http advertised 1.0.1 per-package and 1.0.0 in the index -- so
the index is generated from the per-package files, which are the richer source.

Run after editing anything in packages/:  python3 build-index.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
INDEX_FIELDS = ("id", "displayName", "description", "repo", "latest", "minEngine",
                "requires", "docs")

def main() -> int:
    entries = []
    for path in sorted((ROOT / "packages").glob("*.json")):
        pkg = json.loads(path.read_text(encoding="utf-8"))
        if pkg["id"] != path.stem:
            print(f"{path.name}: id '{pkg['id']}' does not match filename", file=sys.stderr)
            return 1
        if pkg["latest"] not in pkg.get("versions", []):
            print(f"{path.name}: latest '{pkg['latest']}' is not in versions", file=sys.stderr)
            return 1
        entries.append({k: pkg[k] for k in INDEX_FIELDS})

    index = {"schemaVersion": 1, "packages": entries}
    (ROOT / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"index.json: {len(entries)} packages")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
