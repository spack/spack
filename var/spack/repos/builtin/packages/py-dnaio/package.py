# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDnaio(PythonPackage):
    """Read and write FASTQ and FASTA"""

    homepage = "https://github.com/marcelm/dnaio"
    pypi = "dnaio/dnaio-0.3.tar.gz"
    git = "https://github.com/marcelm/dnaio.git"

    version("0.9.1", sha256="a1a14181995b27197b7e2b8897994a3107c649b9fc2dfe263caff3c455b0d0c4")
    version("0.4.2", sha256="fa55a45bfd5d9272409b714158fb3a7de5dceac1034a0af84502c7f503ee84f8")
    version("0.3", sha256="47e4449affad0981978fe986684fc0d9c39736f05a157f6cf80e54dae0a92638")

    depends_on("py-setuptools@52:", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:", when="@0.4:", type="build")
    # 0.9.1 deps
    depends_on("python@3.7:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-cython@0.29.20:", type=("build", "run"), when="@0.9.1:")
    depends_on("py-xopen@1.4.0:", type=("build", "run"), when="@0.9.1:")
    # older deps
    depends_on("py-xopen", type=("build", "run"))
    depends_on("py-xopen@0.8.2:", when="@0.4:", type=("build", "run"))
