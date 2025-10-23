<!-- SPDX-License-Identifier: MIT -->

# Adding a new version

```console
$ bazel run -- //workflows:versions add X.Y.Z --set_current
```

If you're adding a back-dated version, don't pass `--set_current`.

# Release

```console
$ bazel run -- //workflows:release
```

Then use the GitHub UI to tag the release and attach the source archive (tar.gz)
that was saved to the root of your source tree.
