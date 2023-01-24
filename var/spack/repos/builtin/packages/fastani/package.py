# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastani(AutotoolsPackage):
    """Fast, alignment-free computation of whole-genome Average Nucleotide
    Identity (ANI)"""

    homepage = "https://github.com/ParBLiSS/FastANI"
    url = "https://github.com/ParBLiSS/FastANI/archive/v1.33.tar.gz"

    version("1.33", sha256="0b18b3074094722fb1b2247c1a1c4eb96295fff369b837f422e05072740e0013")

    depends_on("autoconf", type="build")
    depends_on("gsl", type=("build", "link"))
    depends_on("zlib", type=("build", "link"))
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
