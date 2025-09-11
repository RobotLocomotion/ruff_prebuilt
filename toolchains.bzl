# SPDX-License-Identifier: MIT

RuffPrebuiltInfo = provider(
    doc = "XXX",
    fields = ["ruff_executable"],
)

def _ruff_prebuilt_toolchain_impl(ctx):
    toolchain_info = platform_common.ToolchainInfo(
        ruff_prebuilt_info = RuffPrebuiltInfo(
            ruff_executable = ctx.executable.ruff_executable,
        ),
    )
    return [toolchain_info]

ruff_prebuilt_toolchain = rule(
    implementation = _ruff_prebuilt_toolchain_impl,
    attrs = {
        "ruff_executable": attr.label(
            allow_single_file = True,
            cfg = "exec",
            executable = True,
            mandatory = True,
        ),
    },
)

def define_ruff_prebuilt_toolchain(
        *,
        ruff_executable,
        os,
        cpu):
    stem = "ruff_{}_{}".format(os, cpu)
    target_name = "{}_target".format(stem)
    toolchain_name = "{}_toolchain".format(stem)
    ruff_prebuilt_toolchain(
        name = target_name,
        ruff_executable = ruff_executable,
    )
    native.toolchain(
        name = toolchain_name,
        exec_compatible_with = [
            "@platforms//os:{}".format(os),
            "@platforms//cpu:{}".format(cpu),
        ],
        toolchain = ":{}".format(target_name),
        toolchain_type = "@ruff_prebuilt//:toolchain_type",
    )
