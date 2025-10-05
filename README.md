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
    integrity = "sha256-if1EuMaZTepzAZ602iehkxgLNLhaErgtAeti1RVNoR0=",
    strip_prefix = "ruff_prebuilt-0.13.0.1",
    url = "https://github.com/RobotLocomotion/ruff_prebuilt/releases/download/0.13.0.1/ruff_prebuilt-0.13.0.1.tar.gz",
)
```
