# SPDX-License-Identifier: MIT
"""Automates the release process."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from python import runfiles


def _versions_path() -> Path:
    """Returns the source tree path to versions.json."""
    manifest = runfiles.Create()
    path = Path(manifest.Rlocation("_main/versions.json"))
    assert path.exists(), path
    return path.resolve()


def _readme_path() -> Path:
    """Returns the source tree path to README.md."""
    manifest = runfiles.Create()
    path = Path(manifest.Rlocation("_main/README.md"))
    assert path.exists(), path
    return path.resolve()


def _source_tree() -> Path:
    """Returns the source tree root directory."""
    return _versions_path().parent


def _set_module_version(*, module_version):
    """Updates MODULE.bazel's version (on disk)."""
    subprocess.check_call(
        [
            "bazel",
            "run",
            "--",
            "//workflows:buildozer",
            f"set version {module_version}",
            "//MODULE.bazel:ruff_prebuilt",
        ],
        cwd=_source_tree(),
    )


def _sync_module_version() -> str:
    """Updates MODULE.bazel's version to match versions.json ruff version.
    Returns the new version."""
    versions_root = json.loads(_versions_path().read_text(encoding="utf-8"))
    ruff_version = versions_root["current"]
    module_version = f"{ruff_version}.1"
    _set_module_version(module_version=module_version)
    return module_version


def _reset_module_version() -> None:
    """Resets MODULE.bazel's version to the default on the main branch."""
    _set_module_version(module_version="0.0.0.0")


def _make_source_tarball(*, module_version) -> str:
    """Creates a source tarball on disk, and returns its `integrity` value."""
    # Create the archive.
    subprocess.check_call(
        [
            "bazel",
            "build",
            "//workflows:source_archive",
            "--config=release",
        ],
        cwd=_source_tree(),
    )
    # Ask bazel where it put it.
    output_path_str = subprocess.check_output(
        [
            "bazel",
            "cquery",
            "//workflows:source_archive",
            "--config=release",
            "--output=files",
        ],
        cwd=_source_tree(),
        text=True,
        encoding="utf-8",
    )
    # Copy it back to the source tree.
    buried_output_path = _source_tree() / Path(output_path_str.strip())
    output_path = _source_tree() / buried_output_path.name
    shutil.copyfile(buried_output_path, output_path)
    # Compute its checksum.
    hasher = hashlib.sha256()
    hasher.update(output_path.read_bytes())
    digest = base64.b64encode(hasher.digest()).decode("utf-8")
    return f"sha256-{digest}"


def _update_readme_example(*, module_version, integrity) -> None:
    """Updates README.md stanze for example downstream use."""
    path = _readme_path()
    lines = path.read_text(encoding="utf-8").splitlines()

    # Replace `integrity`.
    num_matches = 0
    for i, line in enumerate(lines):
        if line.startswith("    integrity = "):
            num_matches += 1
            new_line = f'    integrity = "{integrity}",'
            lines[i] = new_line
    assert num_matches == 1, num_matches

    # Replace raw version numbers.
    num_matches = 0
    for i, line in enumerate(lines):
        new_line = re.sub(r"(\d+\.\d+\.\d+.\d+)", module_version, line)
        if new_line != line:
            num_matches += 1
            lines[i] = new_line
    assert num_matches == 2, num_matches

    # Write back to the file.
    new_content = "\n".join(lines) + "\n"
    path.write_text(new_content, encoding="utf-8")


def _commit(*, message) -> None:
    """Commits all modified files, using the given message."""
    subprocess.check_call(
        ["git", "add", "MODULE.bazel", "README.md"],
        cwd=_source_tree(),
    )
    subprocess.check_call(
        ["git", "commit", "-m", message],
        cwd=_source_tree(),
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _ = parser.parse_args()
    module_version = _sync_module_version()
    integrity = _make_source_tarball(module_version=module_version)
    _update_readme_example(module_version=module_version, integrity=integrity)
    _commit(message=f"Release {module_version}")
    _reset_module_version()
    _commit(message="Revert back to main branch version numbering")


assert __name__ == "__main__"
main()
