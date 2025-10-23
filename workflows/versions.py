# SPDX-License-Identifier: MIT
"""Automates upkeep of version.json."""

import argparse
import base64
import json
from pathlib import Path
import urllib.request

from python import runfiles

# Maps from rust triples to @platforms//cpu and @platforms//os constants.
_TRIPLE_TO_CPU_OS = {
    "aarch64-apple-darwin": ("aarch64", "macos"),
    "aarch64-pc-windows-msvc": ("aarch64", "windows"),
    "aarch64-unknown-linux-gnu": ("aarch64", "linux"),
    "armv7-unknown-linux-gnueabihf": ("armv7", "linux"),
    "i686-pc-windows-msvc": ("x86_32", "windows"),
    "i686-unknown-linux-gnu": ("x86_32", "linux"),
    "powerpc64le-unknown-linux-gnu": ("ppc64le", "linux"),
    "riscv64gc-unknown-linux-gnu": ("riscv64", "linux"),
    "s390x-unknown-linux-gnu": ("s390x", "linux"),
    "x86_64-apple-darwin": ("x86_64", "macos"),
    "x86_64-pc-windows-msvc": ("x86_64", "windows"),
    "x86_64-unknown-linux-gnu": ("x86_64", "linux"),
}


def _versions_path() -> Path:
    manifest = runfiles.Create()
    path = Path(manifest.Rlocation("_main/versions.json"))
    assert path.exists(), path
    return path.resolve()


def _download(url: str, *, encoding: str | None) -> bytes:
    with urllib.request.urlopen(url) as response:
        data = response.read()
    if encoding is None:
        return data
    return data.decode(encoding=encoding)


def _sha256_hex_to_integrity(as_hex: str) -> str:
    as_base64 = base64.b64encode(bytes.fromhex(as_hex)).decode("utf-8")
    return f"sha256-{as_base64}"


def _rewrite_versions_json(edits_callback) -> None:
    path = _versions_path()
    root = json.loads(path.read_text(encoding="utf-8"))
    edits_callback(root)
    path.write_text(json.dumps(root, indent=1), encoding="utf-8")


def _add(args: argparse.Namespace) -> None:
    version = args.version
    base_url = f"https://github.com/astral-sh/ruff/releases/download/{version}"
    manifest_url = f"{base_url}/dist-manifest.json"
    manifest = json.loads(_download(manifest_url, encoding="utf-8"))

    download_specs = {}
    for artifact in manifest["artifacts"].values():
        name = artifact["name"]
        if not (name.endswith(".tar.gz") or name.endswith(".zip")):
            continue
        if "target_triples" not in artifact:
            continue
        (triple,) = artifact["target_triples"]
        cpu, os = _TRIPLE_TO_CPU_OS.get(triple, (None, None))
        if cpu is None:
            continue
        sha256_url = f"{base_url}/{name}.sha256"
        sha256_hex = _download(sha256_url, encoding="utf-8").split()[0]
        integrity = _sha256_hex_to_integrity(sha256_hex)
        if name.endswith(".tar.gz"):
            strip_prefix = Path(Path(name).stem).stem
        else:
            strip_prefix = None
        url = f"{base_url}/{name}"
        download_spec = dict(
            cpu=cpu,
            integrity=integrity,
            os=os,
            strip_prefix=strip_prefix,
            urls=[url],
        )
        download_specs[name] = download_spec

    def _edits(root):
        root["available"][version] = dict(downloads=download_specs)
        if args.set_current:
            root["current"] = version

    _rewrite_versions_json(_edits)


def _sync(args: argparse.Namespace) -> None:
    path = _versions_path()
    root = json.loads(path.read_text(encoding="utf-8"))
    versions = list(root["available"].keys())
    for i, version in enumerate(versions):
        print(f"({i + 1}/{len(versions)}) Updating {version}")
        # N.B. Each call to `_add` will write out the modified versions.json.
        # We don't need to write out any changes ourselves.
        _add(
            args=argparse.Namespace(
                version=version,
                set_current=False,
            ),
        )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(required=True)
    parser_add = subparsers.add_parser(
        "add",
        help="Adds a new version to the database (or overwrites the existing one).",
    )
    parser_add.add_argument(
        "version",
        help="The version number to be added (or updated).",
    )
    parser_add.add_argument(
        "--set_current",
        action="store_true",
        help="Sets the new version as current.",
    )
    parser_add.set_defaults(handler=_add)
    parser_sync = subparsers.add_parser(
        "sync",
        help="Updates all versions currently in the database.",
    )
    parser_sync.set_defaults(handler=_sync)
    args = parser.parse_args()
    args.handler(args)


assert __name__ == "__main__"
main()
