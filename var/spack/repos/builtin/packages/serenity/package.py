# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Serenity(CMakePackage):
    """Subsystem focused quantum chemistry code Serenity"""

    homepage = "https://www.uni-muenster.de/Chemie.oc/neugebauer/softwareAKN.html"
    url = "https://github.com/qcserenity/serenity/archive/refs/tags/1.4.0.tar.gz"
    git = "https://github.com/qcserenity/serenity.git"

    version("master", branch="master")
    version("1.4.0", "c7a87fc8e6f8ca21685a27e08d09d49824d9a1e9947fc6abb40d20fbba0cc6e8")

    variant("blas", default=True, description="Use BLAS library with Eigen")
    variant("lapack", default=True, description="Use Lapack library with Eigen")
    variant("python", default=False, description="Build Python bindings")

    depends_on("blas", when="+blas")
    depends_on("cmake@3.12:", type="build")
    depends_on("boost")
    depends_on("eigen@3:")
    depends_on("googletest@1.8.1:", type="test")
    depends_on("hdf5@1.10.1:")
    depends_on("lapack", when="+lapack")
    depends_on("libecpint")
    depends_on("libxc@5.0.0")
    depends_on("pkgconfig", type="build")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11", when="+python", type="build")
    depends_on("serenity-libint")
    depends_on("xcfun")

    extends("python", when="+python")

    def patch(self):
        filter_file(
            "include(CMakeParseArguments)",
            'message(FATAL_ERROR "Tried to download a dependency")',
            "cmake/DownloadProject.cmake",
            string=True,
        )

        if self.run_tests:
            filter_file(
                "find_package(GTest 1.8.1 QUIET)",
                "find_package(GTest REQUIRED)",
                "cmake/ImportGTest.cmake",
                string=True,
            )

            filter_file(
                "find_package(GMock 1.8.1 QUIET)",
                "return()",
                "cmake/ImportGTest.cmake",
                string=True,
            )

        filter_file(
            "function(import_libecpint)",
            "function(import_libecpint)\n"
            "find_package(ecpint CONFIG REQUIRED)\n"
            "add_library(ecpint INTERFACE IMPORTED)\n"
            "target_link_libraries(ecpint INTERFACE ECPINT::ecpint)\n",
            "cmake/ImportLibecpint.cmake",
            string=True,
        )

        filter_file(
            "function(import_libint)",
            "function(import_libint)\n"
            "find_package(Libint2 CONFIG REQUIRED)\n"
            "add_library(libint2-static INTERFACE IMPORTED)\n"
            "target_link_libraries(libint2-static INTERFACE Libint2::libint2)\n",
            "cmake/ImportLibint.cmake",
            string=True,
        )

        filter_file(
            "function(import_libxc)",
            "function(import_libxc)\n"
            "find_package(PkgConfig QUIET)\n"
            "pkg_check_modules(pc_libxc libxc)\n"
            "if(pc_libxc_FOUND)\n"
            "add_library(xc INTERFACE IMPORTED)\n"
            "target_link_libraries(xc INTERFACE ${pc_libxc_LINK_LIBRARIES})\n"
            "target_include_directories(xc INTERFACE ${pc_libxc_INCLUDE_DIRS})\n"
            "endif()",
            "cmake/ImportLibxc.cmake",
            string=True,
        )

        filter_file(
            "function(import_pybind11)",
            "function(import_pybind11)\nfind_package(pybind11 REQUIRED)",
            "cmake/ImportPybind11.cmake",
            string=True,
        )

        filter_file(
            "function(import_xcfun)",
            "function(import_xcfun)\n"
            "find_package(XCFun CONFIG REQUIRED)\n"
            "add_library(xcfun INTERFACE IMPORTED)\n"
            "target_link_libraries(xcfun INTERFACE XCFun::xcfun)\n",
            "cmake/ImportXCFun.cmake",
            string=True,
        )

    def cmake_args(self):
        args = [
            self.define("SERENITY_BUILD_TESTS", self.run_tests),
            self.define_from_variant("SERENITY_BUILD_PYTHON_BINDINGS", "python"),
            self.define("SERENITY_MARCH", ""),
            self.define("SERENITY_PREFER_XCFUN", False),
            self.define("SERENITY_USE_XCFUN", True),
            self.define("SERENITY_USE_LIBXC", True),
            self.define(
                "SERENITY_USE_INTEL_MKL", self.spec["lapack"].libs.names[0].startswith("mkl")
            ),
            self.define_from_variant("SERENITY_USE_LAPACK", "lapack"),
            self.define_from_variant("SERENITY_USE_BLAS", "blas"),
            self.define("SERENITY_USAGE_FROM_SOURCE", False),
            self.define("Libint2_DIR", self.spec["serenity-libint"].prefix.lib.cmake.libint2),
            self.define("XCFun_DIR", self.spec["xcfun"].prefix.share.XCFun),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
        if "+python" in self.spec:
            args.append(self.define("PYTHON_EXECUTABLE", self.spec["python"].command.path))
        return args
