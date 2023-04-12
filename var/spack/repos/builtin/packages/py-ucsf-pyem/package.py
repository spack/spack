# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUcsfPyem(PythonPackage):
    """UCSF pyem is a collection of Python modules and command-line
    utilities for electron microscopy of biological samples."""

    homepage = "https://github.com/asarnow/pyem"
    git = "https://github.com/asarnow/pyem.git"

    maintainers("dorton21")

    # Using commit since releases haven't been updated in 2 years
    version("2021-04-07", commit="ed0527f98657d21d887357426b74e5240d477fae")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.14:", type=("build", "run"))
    depends_on("py-scipy@1.2:", type=("build", "run"))
    depends_on("py-matplotlib@2.2:", type=("build", "run"))
    depends_on("py-future@0.15:", type=("build", "run"))
    depends_on("py-numba@0.41:", type=("build", "run"))
    depends_on("py-seaborn@0.9:", type=("build", "run"))
    depends_on("py-pandas@0.23.4:", type=("build", "run"))
    depends_on("py-pathos@0.2.1:", type=("build", "run"))
    depends_on("py-pyfftw@0.10:", type=("build", "run"))
    depends_on("py-healpy@1.11:", type=("build", "run"))
    depends_on("py-natsort@6.0:", type=("build", "run"))

    # Extracts files into bin for proper useage
    @run_after("install")
    def extraction(self):
        mkdir(self.prefix.bin)
        install("*.py", self.prefix.bin)
