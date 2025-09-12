<!-- SPDX-License-Identifier: MIT -->

# Using

Add this to your `MODULE.bazel` and then you can refer to the label `"@ruff"`
for the `ruff` executable.


```bzl
bazel_dep(
    name = "ruff_prebuilt",
    repo_name = "ruff",
    dev_dependency = True,
)
archive_override(
    module_name = "ruff_prebuilt",
    integrity = "sha256-0000000000000000000000000000000000000000000=",
    strip_prefix = "ruff_prebuilt-GIT_SHA",
    url = "https://github.com/RobotLocomotion/ruff_prebuilt/archive/GIT_SHA.tar.gz",
)
```
