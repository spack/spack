# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyedr(PythonPackage):
    """Reads Gromacs EDR file to populate a pandas dataframe"""

    homepage = "https://github.com/MDAnalysis/panedr"
    pypi = "pyedr/pyedr-0.7.1.tar.gz"

    maintainers("RMeli")

    version("0.7.1", sha256="ad7ccdeb739399acd11a25f2d2413ebb46a54223059a2b902ac604d29fabd767")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.19.0:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
