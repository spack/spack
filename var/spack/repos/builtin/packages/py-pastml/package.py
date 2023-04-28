# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPastml(PythonPackage):
    """Ancestral character reconstruction and visualisation for rooted
    phylogenetic trees.
    """

    homepage = "https://github.com/evolbioinfo/pastml"
    pypi = "pastml/pastml-1.9.40.tar.gz"

    maintainers("snehring")

    version("1.9.40", sha256="5334bc8de70a968117240b90d90878ac935be18de6e6e485fb1a8f90cd539fea")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-ete3@3.1.1:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"))
    depends_on("py-jinja2@2.11.0:", type=("build", "run"))
    depends_on("py-scipy@1.5.0:", type=("build", "run"))
    depends_on("py-itolapi@4.0.0:", type=("build", "run"))
    depends_on("py-biopython@1.70:", type=("build", "run"))
