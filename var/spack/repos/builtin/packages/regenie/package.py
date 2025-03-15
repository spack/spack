# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Regenie(CMakePackage):
    """regenie is a C++ program for whole genome regression modelling of large genome-wide
    association studies."""

    homepage = "https://rgcgithub.github.io/regenie/"
    url = "https://github.com/rgcgithub/regenie/archive/refs/tags/v4.1.tar.gz"

    maintainers("teaguesterling")

    license("MIT", checked_by="teaguesterling")

    version("4.1", sha256="a7d8ad321ca66bd10fa5ed651c63069886f5cb5ef8e900ca9a0c5b7e3dfc7da5")

    variant("boostio", default=True, description="Build with Boost IO support")
    variant("static", default=False, description="Build a statically linked version")
    variant("builtin-eigen", default=False, description="Build with vendored eigen library")
    variant("builtin-cxxopts", default=False, description="Build with vendored cxxopts library")
    variant("builtin-lbfgspp", default=False, description="Build with vendored LBFGSpp library")
    variant(
        "bgen-builtins", default=False, description="Build with sqlite, boost, and zstd from bgen"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("zlib")  # Not zlib-api
    depends_on("openssl")
    depends_on("bzip2")
    depends_on("lzma")
    depends_on("libdeflate")
    depends_on("netlib-lapack+lapacke+external-blas")
    depends_on("openblas threads=openmp")
    depends_on("htslib")
    depends_on("htslib+pic", when="+static")
    depends_on("python@3")
    depends_on("bgen+source")
    depends_on("cmake@3.13:")
    depends_on("boost+iostreams", when="+boostio")
    depends_on("eigen@3.4:", when="~builtin-eigen")
    depends_on("cxxopts@3", when="~builtin-cxxopts")
    depends_on("cxxopts@3.0", when="~builtin-cxxopts+bgen-builtins")
    depends_on("lbfgspp", when="~builtin-lbfgspp")

    with when("~bgen-builtins"):
        depends_on("zstd")
        depends_on("sqlite@3")
        depends_on("boost@1.55+chrono+date_time+exception+filesystem+math+system+thread+timer")
        depends_on("zstd libs=static", when="+static")
        with when("~static"):
            depends_on("zstd libs=shared")
            depends_on("boost+shared")

    def patch(self):
        satisfies = self.spec.satisfies

        def dep_dirs(dep):
            return " ".join(f'"{d}"' for d in dep.directories)

        # Avoid accidentally linking against system
        filter_file("-L/usr/lib", "", "Makefile")  # Don't explictly link system
        filter_file("-Wno-c11-extensions", "", "CMakeLists.txt")  # Flag doesn't exist

        # libcrypt needs to be defined explicitly and libssl needs to be linked
        # before everything else or symbols will not be found
        ssl = self.spec["openssl"]
        filter_file(
            r"  find_library\(CRYPTO_LIB crypto REQUIRED\)",
            f"  find_library(CRYPTO_LIB crypto HINTS {dep_dirs(ssl.libs)})\n"
            f"  find_library(SSL_LIB ssl HINTS {dep_dirs(ssl.libs)})\n"
            "  target_link_libraries(regenie PUBLIC ${SSL_LIB})",
            "CMakeLists.txt",
        )
        # libblas needs to be defined before lapack
        filter_file(
            r"\$\{LAPACK_LIB\} -llapacke \$\{BLAS_LIB\}",
            "${BLAS_LIB} ${LAPACK_LIB} -llapacke",
            "CMakeLists.txt",
        )

        # Record any libraries that will be statically linked by default
        statics = ["hts"]
        statics_lib_overrides = {
            "boost": [
                "boost_chrono",
                "boost_exception",
                "boost_date_time",
                "boost_filesystem",
                "boost_math",
                "boost_system",
                "boost_thread",
                "boost_timer",
            ]
        }

        if satisfies("+boostio"):
            statics_lib_overrides["boost"].append("boost_iostreams")

        # Avoid using (some) vendored dependencies included with regenie
        for dep, old_path in [
            ("eigen", r"\$\{EXTERN_LIBS_PATH\}/eigen-3.4.0/"),
            ("cxxopts", r"\$\{EXTERN_LIBS_PATH\}/cxxopts/include/"),
            ("lbfgspp", r"\$\{EXTERN_LIBS_PATH\}/LBFGSpp/include/"),
        ]:
            if self.spec.satisfies(f"~builtin-{dep}"):
                lib = self.spec[dep]
                filter_file(old_path, dep_dirs(lib.headers), "CMakeLists.txt")

        # Avoid using vendored dependencies distribued with bgen
        if satisfies("~bgen-builtins"):
            for dep, lib_name, old_lib, old_inc in [
                ("zstd", "zstd", "zstd-1.1.0", "zstd-1.1.0/lib"),
                ("sqlite", "sqlite3", "sqlite3", "sqlite3"),
                ("boost", "boost", "boost_1_55_0", "boost_1_55_0/"),
            ]:
                lib = self.spec[dep]
                lib_pat = f'"\\$\\{{BGEN_PATH\\}}/build/3rd_party/{old_lib}"'
                inc_pat = f"\\$\\{{BGEN_PATH\\}}/3rd_party/{old_inc}"
                filter_file(lib_pat, dep_dirs(lib.libs), "CMakeLists.txt")
                filter_file(inc_pat, dep_dirs(lib.headers), "CMakeLists.txt")
                statics.append(lib_name)

        # Convert static libraries to shared unless we are actually building static
        if satisfies("~static"):
            for lib_name in statics:
                if lib_name in statics_lib_overrides:
                    lib_override = " ".join(statics_lib_overrides[lib_name])
                else:
                    lib_override = lib_name
                filter_file(f"lib{lib_name}\\.a", lib_override, "CMakeLists.txt")
        elif satisfies("~bgen-builtins"):
            for lib_name, overrides in statics_lib_overrides.items():
                override = [f"lib{override}.a" for override in statics_lib_overrides[lib_name]]
                filter_file(f"lib{lib_name}\\.a", " ".join(override), "CMakeLists.txt")

    def setup_build_environment(self, env):
        bgen = self.spec["bgen"]
        htslib = self.spec["htslib"]
        openblas = self.spec["openblas"]
        env.set("BGEN_PATH", bgen.prefix.src.bgen)
        env.set("HTSLIB_PATH", htslib.prefix.lib)
        env.set("OPENBLAS_ROOT", openblas.prefix)
        env.set("STATIC", "1" if self.spec.satisfies("+static") else "0")
        env.set("HAS_BOOST_IOSTREAM", "1" if self.spec.satisfies("+boostio") else "0")
