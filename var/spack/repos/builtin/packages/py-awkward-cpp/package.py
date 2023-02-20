# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwkwardCpp(PythonPackage):
    """py-awkward-cpp provides precompiled routines for the py-awkward package.
    It is not useful on its own, only as a dependency for py-awkward."""

    git = "https://github.com/scikit-hep/awkward.git"
    pypi = "awkward-cpp/awkward-cpp-9.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers("vvolkl", "wdconinc")

    version("9", sha256="db1c91c21f88b89a39b46176edc67a08b37f7283c16a2ed5159e3c874613c61a")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-scikit-build-core@0.2:", type="build")
    depends_on("py-pybind11", type=("build", "link"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"))
