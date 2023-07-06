# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyrad(PythonPackage):
    """An interactive toolkit for assembly and analysis of restriction-site
    associated genomic data sets (e.g., RAD, ddRAD, GBS) for population
    genetic and phylogenetic studies."""

    homepage = "https://github.com/dereneaton/ipyrad"

    url = "https://github.com/dereneaton/ipyrad/archive/refs/tags/0.9.85.tar.gz"

    version("0.9.90", sha256="8b95aa3bae30da15baba90abb03176932411ff708c54d5e4481b811cceb8a4a8")
    version("0.9.85", sha256="17b07466531655db878919e426743ac649cfab2e92c06c4e45f76ee1517633f9")

    depends_on("py-setuptools", type="build")

    # Dependencies found at
    # https://ipyrad.readthedocs.io/en/master/3-installation.html#details-dependencies
    depends_on("bedtools2", type=("build", "run"))
    depends_on("bwa", type=("build", "run"))
    depends_on("muscle", type=("build", "run"))
    depends_on("py-notebook", type=("build", "run"))
    depends_on("samtools", type=("build", "run"))
    depends_on("vsearch", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-ipyparallel", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-cutadapt", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))

    def patch(self):
        # ipyrad/core/Parallel.py assumes that ipcluster will always be
        # in the python root
        filter_file(
            r"^IPCLUSTER_BIN\s*=.*$",
            'IPCLUSTER_BIN = "{}"'.format(self.spec["py-ipyparallel"].prefix.bin.ipcluster),
            join_path("ipyrad", "core", "Parallel.py"),
        )
