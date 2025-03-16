# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bgen(WafPackage):
    """This repository contains a reference implementation of the BGEN format, written
    in C++. The library can be used as the basis for BGEN support in other software,
    or as a reference for developers writing their own implementations of the BGEN format.

    If you make use of the BGEN library, its tools or example programs, please cite:

    Band, G. and Marchini, J., "BGEN: a binary file format for imputed genotype and
    haplotype data", bioArxiv 308296; doi: https://doi.org/10.1101/308296."""

    homepage = "https://enkre.net/cgi-bin/code/bgen"

    license("BSL-1.0")
    maintainers("teaguesterling")

    version(
        "1.1.7",
        sha256="121f5956f04ad174bc410fa7deed59e2ebff0ec818a3c66cf5d667357dddfb62",
        url="https://enkre.net/cgi-bin/code/bgen/tarball/6ac2d582f9/BGEN-6ac2d582f9.tar.gz",
    )

    variant("headers", default=True, description="Install headers")
    variant("libs", default=True, description="Install static libraries")
    variant("bundled-deps", default=False, description="Use bundled 3rd party dependencies")
    variant("full-source", default=False, description="Install source tree as well")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fossil", type="build")
    depends_on("zlib-api")

    with when("~bundled-deps"):
        # Upper bound of boost not known. Doesn't work with 1.85
        depends_on(
            "boost@1.55:+chrono+date_time+exception+filesystem+math+system+thread+timer+shared"
        )
        depends_on("sqlite@3")
        depends_on("zstd libs=shared,static")
        patch("dont-build-with-bundled-deps.patch")

    def flag_handler(self, name, flags):
        # Version 1.1.7 not compatible with C++17
        if name == "cxxflags":
            flags.append("-std=c++11")
        elif name == "ldflags":
            deps = ["zlib-api"]
            if self.spec.satisfies("~bundled-deps"):
                deps += ["boost", "zstd", "sqlite"]
            for dep in deps:
                flags.append(self.spec[dep].libs.ld_flags)
        return (flags, None, None)

    def patch(self):
        filter_file("-Wno-c++11-long-long", "", "wscript", string=True)  # Creates lots of noise

        if self.spec.satisfies("^boost@1.56:"):
            filter_file(
                "(total_count == 0)",
                "(*total_count == 0)",
                "appcontext/src/CmdLineUIContext.cpp",
                string=True,
            )

        # Update build script to remove references to bundled dependencies
        if self.spec.satisfies("~bundled-deps"):
            for dep, old_include in [
                ("boost", '"3rd_party/boost_1_55_0/boost/"'),
                ("zstd", '"3rd_party/zstd-1.1.0/"'),
                ("sqlite", '"3rd_party/sqlite3/"'),
            ]:
                header_dirs = self.spec[dep].headers.directories
                new_include = ", ".join(f'"{d}"' for d in header_dirs)
                filter_file(old_include, new_include, "wscript")
            filter_file(
                '"sqlite3/sqlite3.h"',
                "<sqlite3.h>",
                "db/include/db/SQLite3Connection.hpp",
                "db/include/db/SQLite3Statement.hpp",
                "db/include/db/SQLStatement.hpp",
                "db/src/SQLite3Statement.cpp",
                "db/src/SQLStatement.cpp",
                string=True,
            )

    def install(self, spec, prefix):
        super().install(spec, prefix)
        if spec.satisfies("+headers"):
            for src in ["appcontext", "db", "genfile"]:
                include_dir = join_path(self.stage.source_path, src, "include")
                src_dir = join_path(self.stage.source_path, src, "src")
                code_dir = join_path(prefix.src.bgen, src)
                install_tree(include_dir, prefix.include.bgen)
                if src not in ["genfile"]:
                    install_tree(src_dir, code_dir)

        if spec.satisfies("+libs"):
            mkdirp(prefix.lib.bgen.db)
            build_dir = join_path(self.stage.source_path, "build")
            install(join_path(build_dir, "libbgen.a"), prefix.lib.bgen)
            install(join_path(build_dir, "db/libdb.a"), prefix.lib.bgen.db)

        if spec.satisfies("+full-source"):
            src_dir = join_path(prefix.opt.src.bgen)
            makedirs(src_dir)
            install_tree(self.stage.source_path, src_dir)

    @property
    def bgen_static_lib_dir(self):
        return self.install.lib.bgen
