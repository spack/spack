# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dftd4(MesonPackage):
    """Generally Applicable Atomic-Charge Dependent London Dispersion Correction"""

    homepage = "https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/dftd4"
    url = "https://github.com/dftd4/dftd4/archive/refs/tags/v3.2.0.tar.gz"
    git = "https://github.com/dftd4/dftd4.git"

    version("main", branch="main")
    version("3.2.0", "9874db9e2329519db258dd75ee7ce7c97947f975b00087ba5fdf9a28741088f1")
    version("3.1.0", "cba67cce1ebd194e844c582b3ebec250ba7d349894ee6e8052686e39c70131ce")
    version("3.0.0", "6db4ee4c815dbafd5e2efb6f35259798a0b99057ec0e7c40f0cc5a91c094e08e")

    variant("openmp", default=True, description="Use OpenMP parallelisation")
    variant("python", default=False, description="Build Python extension module")

    depends_on("blas")
    depends_on("cmake", type="build")
    depends_on("lapack")
    depends_on("meson@0.57.1:", type="build")  # mesonbuild/meson#8377
    depends_on("pkgconfig", type="build")
    depends_on("py-cffi", when="+python")
    depends_on("python@3.6:", when="+python")

    def meson_args(self):
        lapack = self.spec["lapack"].libs.names[0]
        if lapack == "lapack":
            lapack = "netlib"
        elif lapack.startswith("mkl"):
            lapack = "mkl"
        elif lapack != "openblas":
            lapack = "auto"

        return [
            "-Dlapack={0}".format(lapack),
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
            "-Dpython={0}".format(str("+python" in self.spec).lower()),
        ]
