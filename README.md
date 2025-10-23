<!-- SPDX-License-Identifier: MIT -->

# Using

Add this to your `MODULE.bazel` and then you can refer to the label `"@ruff"`
for the `ruff` executable.


```bzl
bazel_dep(
    name = "ruff_prebuilt",
    version = "0.14.1.3",
    dev_dependency = True,
    repo_name = "ruff",
)
```
