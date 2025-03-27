# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5zZfp(CMakePackage):
    """A highly flexible floating point and integer compression plugin for the
    HDF5 library using ZFP compression."""

    homepage = "https://h5z-zfp.readthedocs.io/en/latest"
    git = "https://github.com/LLNL/H5Z-ZFP.git"
    url = "https://github.com/LLNL/H5Z-ZFP/archive/refs/tags/v1.1.1.tar.gz"

    maintainers("markcmiller86", "brtnfld", "byrnHDF")

    version("develop", branch="master")
    version("1.1.1", sha256="921af7b9d1c8c46c036b46544f2785f69d405c0701abe1c1ce3aca2bd5899171")
    version("1.1.0", sha256="48a81e69d1f3b61d9a1eb07e868164fadf3b88690ec930efd849f5889681a893")

    depends_on("c", type="build")
    depends_on("fortran", type="build", when="+fortran")

    variant("fortran", default=True, description="Enable Fortran support")
    variant("shared", default=True, description="Build shared libraries")
    variant("tests", default=False, description="Build tests")

    depends_on("hdf5")
    depends_on("zfp bsws=8")
    depends_on("hdf5+fortran", when="+fortran")
    depends_on("mpi", when="^hdf5+mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("FORTRAN_INTERFACE", "fortran"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]

        return args
