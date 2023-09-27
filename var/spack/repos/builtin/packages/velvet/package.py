# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def is_positive_int(x):
    if isinstance(x, int) and x>0:
        return True
    else:
        return False

class Velvet(MakefilePackage):
    """Velvet is a de novo genomic assembler specially designed for short read
    sequencing technologies."""

    homepage = "https://www.ebi.ac.uk/~zerbino/velvet/"
    url = "https://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.10.tgz"

    version("1.2.10", sha256="884dd488c2d12f1f89cdc530a266af5d3106965f21ab9149e8cb5c633c977640")

    variant("maxkmerlength", default=31,
            description="Longest kmer size you can use in an analysis",
            values=is_positive_int)

    depends_on("zlib-api")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        if spec.target.family == "aarch64":
            makefile.filter("-m64", "")
        maxkmerlength = self.spec.variants["maxkmerlength"].value
        makefile.filter('^MAXKMERLENGTH\s*=\s*.*', f'MAXKMERLENGTH = {maxkmerlength}')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("velvetg", prefix.bin)
        install("velveth", prefix.bin)
