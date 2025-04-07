# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mopac
#
# You can edit this file again by typing:
#
#     spack edit mopac
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Mopac(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://openmopac.net/"
    url = "https://github.com/openmopac/mopac/archive/refs/tags/v23.1.2.tar.gz"
    git = "https://github.com/openmopac/mopac.git"

    maintainers("RMeli")

    license("Apache-2.0", checked_by="RMeli")

    version("main", branch="main")
    version("23.1.2", sha256="60436bbf62045f06f17b4604bf241c8c6359a70a89c41d00913833bf32ea0121")

    variant("static", default=False, description="Build static libraries")
    variant("cmalloc", default=False, description="Use C malloc/free for API memory management")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("tests", default=False, description="Enable test suite")

    depends_on("fortran", type="build")
    depends_on("c", type="build", when="^[virtuals=blas,lapack] intel-oneapi-mkl")
    depends_on("c", type="build", when="+cmalloc")

    depends_on("blas")
    depends_on("lapack")

    depends_on("python", when="+tests")
    depends_on("py-numpy", when="+tests")

    def cmake_args(self):
        args = [
            self.define_from_variant("STATIC_BUILD", "static"),
            self.define("AUTO_BLAS", "ON"),
            self.define_from_variant("USE_C_MALLOC", "cmalloc"),
            self.define_from_variant("THREADS_KEYWORD", "openmp"),
            self.define_from_variant("TESTS", "tests"),
        ]
        return args
