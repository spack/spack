# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Duckdb(MakefilePackage):
    """DuckDB is an in-process SQL OLAP Database Management System."""

    homepage = "https://duckdb.org"
    url = "https://github.com/duckdb/duckdb/archive/refs/tags/v0.9.2.tar.gz"
    git = "https://github.com/duckdb/duckdb.git"

    license("MIT")
    maintainers("glentner", "teaguesterling")

    version("master", branch="master")
    version("0.10.2", sha256="662a0ba5c35d678ab6870db8f65ffa1c72e6096ad525a35b41b275139684cea6")
    version("0.10.0", sha256="5a925b8607d00a97c1a3ffe6df05c0a62a4df063abd022ada82ac1e917792013")
    version(
        "0.9.2",
        sha256="afff7bd925a98dc2af4039b8ab2159b0705cbf5e0ee05d97f7bb8dce5f880dc2",
        deprecated=True,
    )
    version(
        "0.9.1",
        sha256="37a43188d9354ce3ca101b2b118d867f5f76d04c3b83c09d86fd7508351a631b",
        deprecated=True,
    )
    version(
        "0.9.0",
        sha256="3dbf3326a831bf0797591572440e81a3d6d668f8e33a25ce04efae19afc3a23d",
        deprecated=True,
    )
    version(
        "0.8.1",
        sha256="a0674f7e320dc7ebcf51990d7fc1c0e7f7b2c335c08f5953702b5285e6c30694",
        deprecated=True,
    )
    version(
        "0.8.0",
        sha256="df3b8e0b72bce38914f0fb1cd02235d8b616df9209beb14beb06bfbcaaf2e97f",
        deprecated=True,
    )
    version(
        "0.7.1",
        sha256="67f840f861e5ffbe137d65a8543642d016f900b89dd035492d562ad11acf0e1e",
        deprecated=True,
    )

    depends_on("python@3.7:")
    depends_on("cmake", type="build")
    depends_on("gmake", type="build")
    depends_on("ninja", when="+ninjabuild", type="build")
    depends_on("openssl", when="+httpfs")
    depends_on("icu4c", when="~icu")

    # Build Options
    variant("autocomplete", default=True, description="Include autocomplete for CLI in build")
    variant("cli", default=True, description="Compile with command line client")
    variant("icu", default=False, description="Compile with bundled ICU library")
    variant("ninjabuild", default=True, description="Use GEN=ninja to build")
    variant(
        "openssl",
        default=False,
        description="Compile with bundled OpenSSL library",
        when="@:0.9.2",
    )

    # Extensions
    variant("excel", default=True, description="Include Excel formatting extension in build")
    variant("fts", default=True, description="Include FTS (full text search) support in build")
    variant("httpfs", default=True, description="Include HTTPFS (& S3) support in build")
    variant("inet", default=True, description="Include INET (ip address) support in build")
    variant("json", default=True, description="Include JSON support in build")
    variant("parquet", default=True, description="Include parquent support in build")

    # APIs
    variant("jdbc", default=False, description="Build JDBC driver (may not work)")
    variant("odbc", default=False, description="Build with ODBC driver (may not work)")
    variant("python", default=False, description="Build with Python driver (may not work)")

    def setup_build_environment(self, env):
        if "+ninjabuild" in self.spec:
            env.set("GEN", "ninja")
        variant_flags = [
            "autocomplete",
            "cli",
            "excel",
            "fts",
            "httpfs",
            "icu",
            "inet",
            "jdbc",
            "json",
            "odbc",
            "openssl",
            "parquet",
            "python",
        ]
        for flag in variant_flags:
            make_flag = "BUILD_" + flag.upper()
            if "+" + flag in self.spec:
                env.set(make_flag, "1")
            elif "~" + flag in self.spec:
                env.set(make_flag, "0")
        if self.spec.satisfies("@0.10.2:"):
            env.set("OVERRIDE_GIT_DESCRIBE", f"v{self.spec.version}")

    def url_for_version(self, version):
        return "https://github.com/duckdb/duckdb/archive/refs/tags/v{0}.tar.gz".format(version)

    def patch(self):
        # DuckDB pulls its version from a git tag, which it can't find in the tarball
        # and thus defaults to something arbitrary and breaks extensions.
        # We use the Spack version to inject it in the right place during the build
        # Patching is not needed for versions from 0.10.2 onward as we can
        # set OVERRIDE_GIT_DESCRIBE to force the version when not building from a repo.

        version = self.spec.version
        if self.spec.satisfies("@:0.9.2"):
            # Prior to version 0.10.0, this was sufficient
            filter_file(
                r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\}, '
                r'version \$\{DUCKDB_VERSION\}"\))',
                'set(DUCKDB_VERSION "v{0}")\n\\1'.format(version),
                "CMakeLists.txt",
            )
        elif not self.spec.satisfies("@0.10.0"):
            # Override the fallback values that are set when GIT_COMMIT_HASH doesn't work
            for i, n in enumerate(["MAJOR", "MINOR", "PATCH"]):
                filter_file(
                    r"set\(DUCKDB_{0}_VERSION \d+\)".format(n),
                    "set(DUCKDB_{0}_VERSION {1})".format(n, version[i]),
                    "CMakeLists.txt",
                )
            # Need to manually set DUCKDB_NORMALIZED_VERSION for helper scripts
            filter_file(
                r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\},'
                r" version \$\{DUCKDB_VERSION\},"
                r' extension folder \$\{DUCKDB_NORMALIZED_VERSION\}"\))',
                'set(DUCKDB_VERSION "v${DUCKDB_MAJOR_VERSION}'
                '.${DUCKDB_MINOR_VERSION}.${DUCKDB_PATCH_VERSION}")'
                '\nset(DUCKDB_NORMALIZED_VERSION "${DUCKDB_VERSION}")'
                "\n\\1",
                "CMakeLists.txt",
            )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("build/release/duckdb", prefix.bin)
