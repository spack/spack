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

    variant("with-boostio", default=True, description="Build with Boost IO support")
    variant("with-htslib", default=True, description="Build with HTSLib support")
    variant("static", default=False, description="Build a statically linked version")
    variant("bundled-eigen", default=False, description="Build with vendored eigen library")
    variant("bundled-cxxopts", default=False, description="Build with vendored cxxopts library")
    variant("bundled-lbfgspp", default=False, description="Build with vendored LBFGSpp library")
    variant(
        "bgen-bundled-deps",
        default=False,
        description="Build with sqlite, boost, and zstd from bgen",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("cmake@3.13:", type="build")
    depends_on("zlib-api")
    depends_on("openssl")
    depends_on("bzip2")
    depends_on("lzma")
    depends_on("libdeflate")
    depends_on("python")
    depends_on("netlib-lapack+lapacke+external-blas")
    depends_on("openblas threads=openmp")
    depends_on("bgen+headers+libs", when="~bgen-bundled-deps")
    depends_on("bgen+full-source", when="+bgen-bundled-deps")
    depends_on("boost+iostreams", when="+with-boostio")
    depends_on("eigen@3.4:", when="~bundled-eigen")
    depends_on("cxxopts@3", when="~bundled-cxxopts")
    depends_on("cxxopts@3.0", when="~bundled-cxxopts+bgen-bundled-deps")
    depends_on("lbfgspp", when="~bundled-lbfgspp")

    with when("+with-htslib"):
        depends_on("htslib")
        depends_on("htslib+pic", when="+static")

    with when("~bgen-bundled-deps"):
        depends_on("bgen~bundled-deps")
        depends_on("zstd")
        depends_on("sqlite@3")

        # regenie forces use of C++11 standard, boost::math requires C++14 after v1.82
        depends_on(
            "boost@1.55:1.81+chrono+date_time+exception+filesystem+math+system+thread+timer"
        )
        depends_on("zstd libs=static", when="+static")
        with when("~static"):
            depends_on("zstd libs=shared")
            depends_on("boost+shared")

    # cxxopts changed the name of the base exception class after 3.0
    # This patch also changed the exception variable from e to msg to avoid any
    # misleading error messages pointing to "e" from boost::math
    patch("fix-cxxopts-with-new-boost.patch", when="^cxxopts@3.1:")

    def patch(self):
        satisfies = self.spec.satisfies

        def dep_dirs(dep):
            return " ".join(f'"{d}"' for d in dep.directories)

        # Avoid accidentally linking against system
        filter_file("-L/usr/lib", "", "Makefile", string=True)  # Don't explictly link system
        filter_file("-Wno-c11-extensions", "", "CMakeLists.txt", string=True)  # Flag doesn't exist

        # libcrypt needs to be defined explicitly and libssl needs to be linked
        # before everything else or symbols will not be found
        ssl = self.spec["openssl"]
        filter_file(
            "  find_library(CRYPTO_LIB crypto REQUIRED)",
            f"  find_library(CRYPTO_LIB crypto HINTS {dep_dirs(ssl.libs)})\n"
            f"  find_library(SSL_LIB ssl HINTS {dep_dirs(ssl.libs)})\n"
            "  target_link_libraries(regenie PUBLIC ${SSL_LIB})",
            "CMakeLists.txt",
            string=True,
        )
        # libblas needs to be defined before lapack
        filter_file(
            "${LAPACK_LIB} -llapacke ${BLAS_LIB}",
            "${BLAS_LIB} ${LAPACK_LIB} -llapacke",
            "CMakeLists.txt",
            string=True,
        )

        # Record any libraries that will be statically linked by default
        statics = ["hts"]

        # Avoid using (some) vendored dependencies included with regenie
        for dep, old_path in [
            ("eigen", r"${EXTERN_LIBS_PATH}/eigen-3.4.0/"),
            ("cxxopts", r"${EXTERN_LIBS_PATH}/cxxopts/include/"),
            ("lbfgspp", r"${EXTERN_LIBS_PATH}/LBFGSpp/include/"),
        ]:
            if self.spec.satisfies(f"~bundled-{dep}"):
                lib = self.spec[dep]
                filter_file(old_path, dep_dirs(lib.headers), "CMakeLists.txt", string=True)

        # Avoid using vendored dependencies distribued with bgen
        if satisfies("~bgen-bundled-deps"):

            # zstd and sqlite can be replaced with subsitutions
            for dep, lib_name, old_lib, old_inc in [
                ("zstd", "zstd", "zstd-1.1.0", "zstd-1.1.0/lib"),
                ("sqlite", "sqlite3", "sqlite3", "sqlite3"),
            ]:
                lib = self.spec[dep]
                lib_pat = f'"${{BGEN_PATH}}/build/3rd_party/{old_lib}"'
                inc_pat = f"${{BGEN_PATH}}/3rd_party/{old_inc}"
                filter_file(lib_pat, dep_dirs(lib.libs), "CMakeLists.txt", string=True)
                filter_file(inc_pat, dep_dirs(lib.headers), "CMakeLists.txt", string=True)
                statics.append(lib_name)

            # Boost needs more careful handling using find_package since bgen created a single
            # static archive that doesn't find/replace as easily
            statics.append("boost")
            boost = self.spec["boost"]
            boost_vers = boost.version.up_to(2)
            boost_comps = [
                "chrono",
                "exception",
                "date_time",
                "filesystem",
                "system",
                "thread",
                "timer",
            ]
            if satisfies("+with-boostio"):
                boost_comps.append("iostreams")
            boost_lib = (
                "find_library(Boost_LIBRARY libboost.a"
                ' HINTS "${BGEN_PATH}/build/3rd_party/boost_1_55_0" REQUIRED)'
            )
            boost_pkg = (
                f"find_package(Boost {boost_vers}" f" COMPONENTS {' '.join(boost_comps)} REQUIRED)"
            )
            for find, replace in [
                (boost_lib, boost_pkg),
                ("${Boost_LIBRARY}", "${Boost_LIBRARIES}"),
                ("${BGEN_PATH}/3rd_party/boost_1_55_0/", "${Boost_INCLUDE_DIR}"),
            ]:
                filter_file(find, replace, "CMakeLists.txt", string=True)

        # Convert static libraries to shared unless we are actually building static
        if satisfies("~static"):
            for lib in statics:
                filter_file(f"lib{lib}.a", lib, "CMakeLists.txt", string=True)

        # The bgen package installs libraries and headers in more traditional locations
        # if we don't use the full source option. Patch the paths for compiling
        bgen = self.spec["bgen"]
        if satisfies("^bgen~full-source"):
            for old_path, new_path in [
                ("${BGEN_PATH}/build", bgen.prefix.lib.bgen),
                (
                    "${BGEN_PATH} ${BGEN_PATH}/genfile/include/",
                    f"{bgen.prefix.include} {bgen.prefix.include.bgen}",
                ),
                ("${BGEN_PATH}/db/include/", bgen.prefix.include.db),
            ]:
                filter_file(old_path, new_path, "CMakeLists.txt", string=True)

    def setup_build_environment(self, env):
        bgen = self.spec["bgen"]
        openblas = self.spec["openblas"]
        env.set("OPENBLAS_ROOT", openblas.prefix)
        if self.spec.satisfies("+static"):
            env.set("STATIC", "1")
        if self.spec.satisfies("+with-boostio"):
            env.set("HAS_BOOST_IOSTREAM", "1")
        if self.spec.satisfies("with-htslib"):
            env.set("HTSLIB_PATH", self.spec["htslib"].prefix.lib)
        if self.spec.satisfies("^bgen~full-source"):
            env.set("BGEN_PATH", bgen.prefix)
        else:
            env.set("BGEN_PATH", bgen.prefix.opt.bgen)
