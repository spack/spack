# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HhSuite(CMakePackage):
    """HH-suite is a widely used open source software suite for
    sensitive sequence similarity searches and protein fold
    recognition. It is based on pairwise alignment of profile Hidden
    Markov models (HMMs), which represent multiple sequence alignments
    of homologous proteins."""

    homepage = "https://github.com/soedinglab/hh-suite"
    url = "https://github.com/soedinglab/hh-suite/archive/refs/tags/v3.3.0.tar.gz"

    version("3.3.0", sha256="dd67f7f3bf601e48c9c0bc4cf1fbe3b946f787a808bde765e9436a48d27b0964")

    variant("mpi", default=True, description="Enable MPI support")

    depends_on("cmake@2.8.12:", type="build")
    depends_on("mpi", when="+mpi")

    def build_args(self, spec, prefix):
        args = []
        if "+mpi" in self.spec:
            args.append("-DCHECK_MPI=1")
        else:
            args.append("-DCHECK_MPI=0")
        return args
