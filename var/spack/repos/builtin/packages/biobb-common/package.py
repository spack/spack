# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BiobbCommon(PythonPackage):
    """Biobb_common is the base package required to use the biobb packages"""

    homepage = "https://github.com/bioexcel/biobb_common"
    git = "https://github.com/bioexcel/biobb_common.git"

    maintainers("d-beltran")

    # Versions
    version("4.0.0", branch="master")

    # Dependencies
    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-biopython@1.78:1.80", type=("build", "run"))

    # Test
    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        python("-c", "import biobb_common")
