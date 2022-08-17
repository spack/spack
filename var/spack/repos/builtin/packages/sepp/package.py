# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sepp(Package):
    """SEPP stands for SATe-enabled phylogenetic placement"""

    homepage = "https://github.com/smirarab/sepp"

    url = "https://github.com/smirarab/sepp/archive/refs/tags/4.5.1.tar.gz"
    maintainers = ["snehring"]

    version("4.5.1", sha256="51e052569ae89f586a1a94c804f09fe1b7910a3ffff7664e2005f18c7d3f717b")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("java@1.8:", type="run")
    depends_on("pasta@1:", type="run")
    depends_on("blast-plus@2.10.1:", type="run")

    def install(self, spec, prefix):
        python = which("python")
        install_tree(".", prefix)
        with working_dir(prefix):
            python("setup.py", "config", "-c")
            python("setup.py", "install")
            python("setup.py", "upp", "-c")
