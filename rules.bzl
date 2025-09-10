def _ruff_binary(ctx):
    info = ctx.toolchains["//:toolchain_type"].ruff_prebuilt_info
    ruff_executable = info.ruff_executable
    ruff = ctx.actions.declare_file("ruff")
    ctx.actions.symlink(
        output = ruff,
        target_file = ruff_executable,
        is_executable = True,
    )
    return [
        DefaultInfo(
            runfiles = ctx.runfiles(files = [ruff]),
            executable = ruff,
        ),
    ]

ruff_binary = rule(
    implementation = _ruff_binary,
    toolchains = ["//:toolchain_type"],
    executable = True,
)
