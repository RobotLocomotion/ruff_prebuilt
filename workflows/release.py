def _versions_path() -> Path:
    manifest = runfiles.Create()
    path = Path(manifest.Rlocation("_main/versions.json"))
    assert path.exists(), path
    return path.resolve()

assert __name__ == "__main__"
main()
