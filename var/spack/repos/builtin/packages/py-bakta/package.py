# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBakta(PythonPackage):
    """Bakta: rapid & standardized annotation
    of bacterial genomes, MAGs & plasmids"""

    homepage = "https://github.com/oschwengers/bakta"
    pypi = "bakta/bakta-1.5.1.tar.gz"

    maintainers("oschwengers")

    license("GPL-3.0-only")

    version("1.5.1", sha256="36781612c4eaa99e6e24a00e8ab5b27dadf21c98ae6d16432f3e78c96a4adb5d")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-biopython@1.78:", type=("build", "run"))
    depends_on("py-xopen@1.1.0:", type=("build", "run"))
    depends_on("py-requests@2.25.1:", type=("build", "run"))
    depends_on("py-alive-progress@1.6.2", type=("build", "run"))
    depends_on("trnascan-se@2.0.8:", type=("build", "run"))
    depends_on("aragorn@1.2.38:", type=("build", "run"))
    depends_on("infernal@1.1.4:", type=("build", "run"))
    depends_on("pilercr@1.06:", type=("build", "run"))
    depends_on("prodigal@2.6.3:", type=("build", "run"))
    depends_on("hmmer@3.3.2:", type=("build", "run"))
    depends_on("diamond@2.0.14:", type=("build", "run"))
    depends_on("blast-plus@2.12.0:", type=("build", "run"))
    depends_on("amrfinder@3.10.23:", type=("build", "run"))
    depends_on("py-deepsig-biocomp@1.2.5:", type=("build", "run"))
