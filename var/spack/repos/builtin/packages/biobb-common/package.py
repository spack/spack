# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BiobbCommon(PythonPackage):
    """Biobb_common is the base package required to use the biobb packages"""

    pypi = "biobb_common/biobb_common-4.0.0.tar.gz"

    maintainers("d-beltran")

    # Versions
    version("4.0.0", sha256="6e13d7d9ebae05f686b625f97a8f28a2b30b08accbbeada5fa3cda7a3036a480")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-biopython@1.78:1.80", type=("build", "run"))
