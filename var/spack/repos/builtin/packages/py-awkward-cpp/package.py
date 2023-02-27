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
    version("8", sha256="a51b554490b3197fc5433822becb2e8208bf78fca82ffa314d839b72b3cc4169")
    version("7", sha256="dde733575b2a5ae5b946fe8667b4ae842d937d3b36ebb383d53dc53ea86ea65d")
    version("6", sha256="58e32afa8aa44c365e764f4b5d07637c79a79be2da7cfbaa3469d8bd26b0bfa2")
    version("5", sha256="e5d6a90d98a14dab36598015e69243b9f83b8851556104cbe778ca9c79923656")
    version("4", sha256="fbc4b5e552873e00ffb6286941efc7b629e4fbc4752e28afb9b54854128937f7")
    version("3", sha256="6070557762bd95d3642ad9c585609db51f899a1e79ce4f41568835efd7d6e066")
    version("2", sha256="5e63f43e3135f76db81e0924a74ecf4870f585c11a9f432568b377c04028868c")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-scikit-build-core@0.1.3:+pyproject", type="build")
    depends_on("py-pybind11", type=("build", "link"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"))
