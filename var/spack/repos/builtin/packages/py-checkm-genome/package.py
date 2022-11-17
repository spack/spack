# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCheckmGenome(PythonPackage):
    """Assess the quality of microbial genomes recovered from isolates, single
    cells, and metagenomes"""

    homepage = "https://ecogenomics.github.io/CheckM"
    pypi = "checkm-genome/checkm-genome-1.0.11.tar.gz"

    version("1.2.1", sha256="33907aa7bbf029f8345e33df80d5c89b7a719041f55ece4f7470cd061c8eff76")
    version("1.0.13", sha256="ffb7e4966c0fac07c7e6e7db6f6eb5b48587fa83987f8a68efbaff2afb7da82e")
    version("1.0.11", sha256="e475d9817d12fa771dbccc80f47758b742fc67c25261dc8ca0c0dc898c2a5190")

    # pip silently replaces distutils with setuptools

    depends_on("python@2.7.0:2.7", type=("build", "run"), when="@:1.0.18")
    depends_on("python@3:", type=("build", "run"), when="@1.1.0:")
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("hmmer@3.1b1:", type=("build", "run"))
    depends_on("pplacer", type=("build", "run"))
    depends_on("prodigal@2.6.1:", type=("build", "run"))
    depends_on("py-backports-functools-lru-cache", type=("build", "run"), when="^python@:3.2")
    depends_on("py-numpy@1.8.0:", type=("build", "run"), when="@0.9.5:1.0.18")
    depends_on("py-numpy@1.21.3:", type=("build", "run"), when="@1.2.0:")
    depends_on("py-scipy@0.9.0:", type=("build", "run"), when="@0.9.5:1.0.18")
    depends_on("py-scipy@1.7.3:", type=("build", "run"), when="@1.2.0")
    depends_on("py-matplotlib@1.3.1:", type=("build", "run"), when="@0.9.5:1.0.18")
    depends_on("py-matplotlib@3.5.1:", type=("build", "run"), when="@1.2.0:")
    depends_on("py-pysam@0.8.3:", type=("build", "run"), when="@1.0.5:1.0.18")
    depends_on("py-pysam@0.19.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("py-dendropy@4.0.0:", type=("build", "run"), when="@1.0.0:1.0.18")
    depends_on("py-dendropy@4.5.2:", type=("build", "run"), when="@1.2.0:")
