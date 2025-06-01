# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCheckmGenome(PythonPackage):
    """Assess the quality of microbial genomes recovered from isolates, single
    cells, and metagenomes"""

    homepage = "https://ecogenomics.github.io/CheckM"
    url = "https://github.com/Ecogenomics/CheckM/archive/refs/tags/v1.2.1.tar.gz"

    maintainers("caelanjmiller")

    license("GPL-3.0-or-later", checked_by="caelanjmiller")
    
    version("1.2.3", sha256="5f8340e71d3256ba8cf407d27bdc7914d1aa86b14b2d63d1e32cceb325e5aa82")
    version("1.2.2", sha256="a748b94e93f8d5fecfd0d5b3f17fcb119b25d4b45217e047b2fd742b21e74c0e")
    version("1.2.1", sha256="2c0b5685bb0fb49813fab16857fd4e0e8c8832b947bbe3a89cf8432659ca945a")

    # pip silently replaces distutils with setuptools
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("hmmer@3.1b1:", type=("build", "run"))
    depends_on("pplacer", type=("build", "run"))
    depends_on("prodigal@2.6.1:", type=("build", "run"))
    depends_on("py-numpy@1.21.3:", type=("build", "run"))
    depends_on("py-scipy@1.7.3:", type=("build", "run"))
    depends_on("py-matplotlib@3.5.1:", type=("build", "run"))
    depends_on("py-pysam@0.19.0:", type=("build", "run"))
    depends_on("py-dendropy@4.5.2:", type=("build", "run"))
