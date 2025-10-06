<!-- SPDX-License-Identifier: MIT -->

# Adding a new version

```console
$ bazel run -- //workflows:versions add X.Y.Z
```

# Release

bazel run -- //workflows:buildozer 'set version 0.14.0.2' //MODULE.bazel:ruff_prebuilt

