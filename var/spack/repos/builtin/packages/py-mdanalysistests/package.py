# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdanalysistests(PythonPackage):
    """Test suite for MDAnalysis"""

    homepage = "https://www.mdanalysis.org"
    pypi = "MDAnalysisTests/MDAnalysisTests-2.4.2.tar.gz"

    maintainers("RMeli")

    version("2.5.0", sha256="a15b53b7f8bed67900a2bf542bbb3cab81dc71674fa6cddb3248dd11880e4c9d")
    version("2.4.3", sha256="6fbdeccdbfb249f76520ee3605d007cd70292187e3754d0184c71e5afe133abb")
    version("2.4.2", sha256="6e8fb210a4268691c77717ea5157e82d85874a4f7ee0f8f177718451a44ee793")

    # Version need to match MDAnalysis'
    depends_on("py-mdanalysis@2.5.0", when="@2.5.0", type=("build", "run"))
    depends_on("py-mdanalysis@2.4.3", when="@2.4.3", type=("build", "run"))
    depends_on("py-mdanalysis@2.4.2", when="@2.4.2", type=("build", "run"))

    depends_on("python@3.9:", when="@2.5.0", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-pytest@3.3.0:", type=("build", "run"))
    depends_on("py-hypothesis", type=("build", "run"))

    depends_on("py-setuptools", type="build")
