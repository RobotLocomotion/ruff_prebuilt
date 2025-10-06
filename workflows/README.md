<!-- SPDX-License-Identifier: MIT -->

# Adding a new version

```console
$ bazel run -- //workflows:versions add X.Y.Z
```

# Release

```console
$ bazel run -- //workflows:release
```

Then use the GitHub UI to tag the release and attach the source archive.
