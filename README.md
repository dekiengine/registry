# Deki package registry

The catalogue the [Deki editor](https://github.com/dekiengine/deki-editor) reads
when you open the Package Manager, and the list it resolves against when a
project asks for a package by id.

It holds no code. Every package lives in its own repository and is installed
from a git tag; this repository only says which packages exist, where they are
and which versions they have.

## Layout

| Path | What it is |
|---|---|
| `packages/<id>.json` | One file per package. The source of truth. |
| `index.json` | The whole catalogue in one file, **generated** from `packages/`. |
| `build-index.py` | Regenerates `index.json`. |

The editor fetches `index.json` first, to list packages, and
`packages/<id>.json` when it needs a package's full version list.

## A package entry

```json
{
  "id": "deki-tween",
  "displayName": "Tween",
  "description": "Animation tweening with 30+ easing functions",
  "repo": "dekiengine/deki-tween",
  "minEngine": "0.16.0",
  "versions": ["0.15.0", "0.16.0"],
  "latest": "0.16.0",
  "requires": [],
  "docs": "https://dekiengine.github.io/deki-tween/"
}
```

`id` must match the filename and the `id` in the package's own `package.json`.
`versions` are git tags on `repo`. `minEngine` is the oldest engine that can
build the package, and the editor checks it in both directions: it refuses a
package needing a newer engine, and one built for an engine older than the
running one supports.

`requires` must list exactly what the package's own `package.json` requires.
The editor's auto-install walks **this** list, so a dependency missing here is
not installed and the project fails to link, with nothing naming the package.

`docs` and `experimental` are optional. The rest are required.

## Adding or updating a package

1. Edit or add `packages/<id>.json`.
2. Run `python build-index.py`.
3. Commit both files. The editor reads `master` directly, so a merge publishes
   it.

`build-index.py` refuses an entry whose `id` disagrees with its filename, or
whose `latest` is not one of its `versions`, and stops on a missing required
field, so those fail before they are published. It cannot check `requires`
against the package's own `package.json`, which lives in another repository,
so that one is on you.

## Releases are in lockstep

The editor, the engine and every package share one version number. A release
bumps all of them together, and `minEngine` names that same number. See
[COMPATIBILITY.md](https://github.com/dekiengine/deki-editor/blob/master/COMPATIBILITY.md).

## License

Apache-2.0. See [LICENSE](LICENSE).
