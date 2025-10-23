<!-- SPDX-License-Identifier: MIT -->

# Using

Add this to your `MODULE.bazel` and then you can refer to the label `"@ruff"`
for the `ruff` executable.


```bzl
bazel_dep(
    name = "ruff_prebuilt",
    dev_dependency = True,
    repo_name = "ruff",
)
archive_override(
    module_name = "ruff_prebuilt",
    integrity = "sha256-kcMC2H4YXB4D3z0hWkuCD0J+q1PSskKbVDLJtK07UJ0=",
    strip_prefix = "ruff_prebuilt-0.14.1.3",
    url = "https://github.com/RobotLocomotion/ruff_prebuilt/releases/download/0.14.1.3/ruff_prebuilt-0.14.1.3.tar.gz",
)
```
