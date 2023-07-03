# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mimalloc(CMakePackage):
    """mimalloc is a compact general purpose allocator with excellent performance."""

    homepage = "https://microsoft.github.io/mimalloc"
    url = "https://github.com/microsoft/mimalloc/archive/v0.0.0.tar.gz"
    git = "https://github.com/microsoft/mimalloc.git"
    maintainers("msimberg")

    version("dev-slice", branch="dev-slice")
    version("dev", branch="dev")
    version("master", branch="master")
    version("2.0.6", sha256="9f05c94cc2b017ed13698834ac2a3567b6339a8bde27640df5a1581d49d05ce5")
    version("1.7.6", sha256="d74f86ada2329016068bc5a243268f1f555edd620b6a7d6ce89295e7d6cf18da")

    depends_on("cmake@3.0:", type="build")

    libs_values = ("shared", "static", "object")
    variant(
        "libs",
        default=",".join(libs_values),
        values=libs_values,
        multi=True,
        description="Build shared, static, or object libraries",
    )

    mimalloc_options = {
        "secure": (
            False,
            "Use full security mitigations (like guard pages, allocation "
            "randomization, double-free mitigation, and free-list corruption "
            "detection)",
            None,
        ),
        "debug_full": (
            False,
            "Use full internal heap invariant checking in DEBUG mode (expensive)",
            None,
        ),
        "padding": (
            True,
            "Enable padding to detect heap block overflow (used only in DEBUG mode)",
            None,
        ),
        "override": (
            True,
            "Override the standard malloc interface (e.g. define entry points "
            "for malloc() etc)",
            None,
        ),
        "xmalloc": (False, "Enable abort() call on memory allocation failure by default", None),
        "show_errors": (
            False,
            "Show error and warning messages by default (only enabled by default "
            "in DEBUG mode)",
            None,
        ),
        "use_cxx": (
            False,
            "Use the C++ compiler to compile the library (instead of the C compiler)",
            None,
        ),
        "see_asm": (False, "Generate assembly files", None),
        "osx_interpose": (
            True,
            "Use interpose to override standard malloc on macOS",
            "platform=darwin",
        ),
        "osx_zone": (
            True,
            "Use malloc zone to override standard malloc on macOS",
            "platform=darwin",
        ),
        "local_dynamic_tls": (
            False,
            "Use slightly slower, dlopen-compatible TLS mechanism (Unix)",
            None,
        ),
        "build_tests": (False, "Build test executables", None),
        "debug_tsan": (False, "Build with thread sanitizer (needs clang)", "%clang"),
        "debug_ubsan": (
            False,
            "Build with undefined-behavior sanitizer (needs clang++)",
            "%clang build_type=Debug +use_cxx",
        ),
        "skip_collect_on_exit": (False, "Skip collecting memory on program exit", None),
    }

    for k, v in mimalloc_options.items():
        if v[2]:
            variant(k, default=v[0], description=v[1], when=v[2])
        else:
            variant(k, default=v[0], description=v[1])

    def cmake_args(self):
        args = [
            self.define("MI_BUILD_%s" % lib.upper(), lib in self.spec.variants["libs"].value)
            for lib in self.libs_values
        ]
        args += [self.define_from_variant("MI_%s" % k.upper(), k) for k in self.mimalloc_options]
        return args
