# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyseer(PythonPackage):
    """Python implementation of Sequence Element Enrichment Analysis (SEER)"""

    homepage = "https://github.com/mgalardini/pyseer"

    url = "https://github.com/mgalardini/pyseer/archive/refs/tags/1.3.11.tar.gz"

    version("1.3.11", sha256="06ea2987509f9c1952bbb90e4b59c6f5a4f2ca9e88e7dac5f5cb7f43aa693a1b")

    # build options
    variant("matplotlib", default=True, description="Enables automatic scree plots")
    variant("dendropy", default=True, description="Enables calculating phylogeny distances")
    variant("kmer", default=True, description="Enables k-mer mapping and annotation")

    # build deps
    depends_on("py-setuptools", type="build")

    # additional deps
    # https://pyseer.readthedocs.io/en/master/installation.html
    # also from
    # github.com/bioconda/bioconda-recipes/blob/master/recipes/pyseer/meta.yaml
    # the deps are messy and this project is not updated
    depends_on("py-numpy@1.15.2:", type=("build", "run"))
    depends_on("py-scipy@1.1.0:", type=("build", "run"))
    depends_on("py-pandas@0.23.4:", type=("build", "run"))
    depends_on("py-scikit-learn@0.20.0:", type=("build", "run"))
    depends_on("py-statsmodels@0.9.0:", type=("build", "run"))
    depends_on("py-pysam@0.15.3:", type=("build", "run"))
    depends_on("py-glmnet-python@1.0", type=("build", "run"))
    depends_on("py-dendropy@4.4.0:", type=("build", "run"))
    depends_on("py-tqdm@4.20.0:", type=("build", "run"))

    # optional deps
    depends_on("py-matplotlib@2.1.0:", when="+matplotlib", type=("build", "run"))
    depends_on("py-dendropy@4.3.0", when="+dendropy", type=("build", "run"))
    depends_on("py-pybedtools@2.27.0:", when="+kmer", type=("build", "run"))
    depends_on("bedops@2.4.9:", when="+kmer", type=("build", "run"))
    depends_on("bwa", when="+kmer", type=("build", "run"))
