<!-- SPDX-License-Identifier: MIT -->

# Using

Add this to your `MODULE.bazel` and then you can refer to the label
`"@ruff_prebuilt//:ruff"`.


```bzl
bazel_dep(
    name = "ruff_prebuilt",
    dev_dependency = True,
)
local_path_override(
    module_name = "ruff_prebuilt",
    path = "/path/to/ruff_prebuilt",
)
```
