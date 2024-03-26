# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"
    pypi = "libsonata/libsonata-0.1.14.tar.gz"

    submodules = True

    maintainers("tristan0x")

    version("develop", branch="master", get_full_repo=True)
    version("0.1.25", sha256="b332efa718123ee265263e1583a5998eaa945a13b8a22903873764cf1d8173fa")

    depends_on("cmake@3.3:", type="build")
    depends_on("hdf5@1.14:")
    depends_on("py-pybind11@2.11:")

    depends_on("py-numpy@1.17.3:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build", when="@0.1:")
    depends_on("py-setuptools-scm@3.4:", type="build", when="@0.1:")

    def patch(self):
        filter_file("EXTLIB_FROM_SUBMODULES", "FALSE", "python/CMakeLists.txt")
