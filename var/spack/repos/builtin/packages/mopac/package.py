# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mopac(CMakePackage):
    """MOPAC (Molecular Orbital PACkage) is a semiempirical quantum chemistry program."""

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
