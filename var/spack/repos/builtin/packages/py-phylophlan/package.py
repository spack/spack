# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhylophlan(PythonPackage):
    """PhyloPhlAn 3.0 is an integrated pipeline for large-scale
    phylogenetic profiling of genomes and metagenomes."""

    homepage = "https://github.com/biobakery/phylophlan"
    pypi = "PhyloPhlAn/PhyloPhlAn-3.0.3.tar.gz"

    version("3.0.3", sha256="a71ff6a1e0b8438da9ca0b6b464573c8d241bc40c87d074120148d46a0b52be4")
    version("3.0.2", sha256="9bb6588721f4e76b9c993b0d3b6a5c3f6cab1d9fe9096dd09f586d732d3e55c1")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-biopython@1.73:", type=("build", "run"))
    depends_on("py-dendropy@4.4.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.15.4:", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-seaborn@0.9.0:", type=("build", "run"))
    depends_on("blast-plus@2.6.0:", type=("build", "run"))
    depends_on("diamond@0.9:", type=("build", "run"))
    depends_on("trimal@1.4.1:", type=("build", "run"))
    depends_on("muscle@3.8.1551:", type=("build", "run"))
    depends_on("mafft@7.310:", type=("build", "run"))
    depends_on("fasttree@2.1.8:", type=("build", "run"))
    depends_on("raxml@8.2.10:", type=("build", "run"))
    depends_on("iqtree2", type=("build", "run"))
    depends_on("mash", type=("build", "run"))
