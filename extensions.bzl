# SPDX-License-Identifier: MIT

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _toolchain_repository_rule_impl(repo_ctx):
    build = """
    load(
        "@ruff_prebuilt//:toolchains.bzl",
        "define_ruff_prebuilt_toolchain",
    )
    """.replace("\n    ", "\n")
    repositories = json.decode(repo_ctx.attr.repositories)
    for repo_name, details in repositories.items():
        binary_name = "ruff.exe" if details["os"] == "windows" else "ruff"
        build += """
        define_ruff_prebuilt_toolchain(
            ruff_executable = "@{repo_name}//:{binary_name}",
            cpu = "{cpu}",
            os = "{os}",
        )
        """.replace("\n        ", "\n").format(
            repo_name = repo_name,
            binary_name = binary_name,
            **details
        )
    repo_ctx.file("BUILD.bazel", build)

_toolchain_repository_rule = repository_rule(
    implementation = _toolchain_repository_rule_impl,
    attrs = {
        "repositories": attr.string(
            doc = "JSON-encoded dictionary of (`repo_name`, `details`) items that communicates the repositories to create and the requirement arguments (i.e., `cpu` and `os`) for each.",
            mandatory = True,
        ),
    },
)

_toolchain_tag_class = tag_class(
    attrs = {
        "name": attr.string(
            doc = "The toolchain name.",
            default = "ruff_prebuilt_toolchain",
        ),
        "versions_json": attr.label(
            doc = "The version lockfile to load for this toolchain.",
            default = "@ruff_prebuilt//:versions.json",
        ),
    },
)

def _sanitize_chars(name):
    # See https://bazel.build/rules/lib/globals/module#module for valid chars.
    result = ""
    for char in name.lower().elems():
        if (("0" <= char) and (char <= "9") or
            ("a" <= char) and (char <= "z") or
            char == "." or
            char == "-" or
            char == "_"):
            result += char
        else:
            result += "_"
    return result

def _per_tag_impl(module_ctx, toolchain_tag):
    versions = json.decode(module_ctx.read(toolchain_tag.versions_json))
    version = versions["current"]
    available = versions["available"]
    downloads = available[version]["downloads"]
    repositories = {}
    for download in downloads.values():
        cpu = download["cpu"]
        os = download["os"]
        integrity = download["integrity"]
        strip_prefix = download["strip_prefix"]
        urls = download["urls"]
        repo_name = "ruff_v{version}_{cpu}_{os}_repo".format(
            version = _sanitize_chars(version),
            os = os,
            cpu = cpu,
        )
        http_archive(
            name = repo_name,
            build_file_content = "exports_files(glob(['**/*']))\n",
            urls = urls,
            integrity = integrity,
            strip_prefix = strip_prefix,
        )
        repositories[repo_name] = struct(
            os = os,
            cpu = cpu,
        )
    _toolchain_repository_rule(
        name = toolchain_tag.name,
        repositories = json.encode(repositories),
    )

def _ruff_prebuilt_extension_impl(module_ctx):
    for module in module_ctx.modules:
        for toolchain_tag in module.tags.toolchain:
            _per_tag_impl(module_ctx, toolchain_tag)
    return module_ctx.extension_metadata(reproducible = True)

ruff_prebuilt_extension = module_extension(
    implementation = _ruff_prebuilt_extension_impl,
    tag_classes = {
        "toolchain": _toolchain_tag_class,
    },
)
