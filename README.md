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
    integrity = "sha256-5z6k9SMm8E4Lgx5UDTHblU7TjA6HEnF7nQkWoSDuYzg=",
    strip_prefix = "ruff_prebuilt-0.14.1.1",
    url = "https://github.com/RobotLocomotion/ruff_prebuilt/releases/download/0.14.1.1/ruff_prebuilt-0.14.1.1.tar.gz",
)
```
