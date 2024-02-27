# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fsa(AutotoolsPackage):
    """FSA is a probabilistic multiple sequence alignment algorithm which uses
    a distance-based approach to aligning homologous protein, RNA or DNA sequences"""

    homepage = "https://fsa.sourceforge.net/"
    url = "https://sourceforge.net/projects/fsa/files/fsa-1.15.9.tar.gz/download"

    license("GPL-2.0-only", checked_by="A-N-Other")

    version("1.15.9", sha256="6ee6e238e168ccba0d51648ba64d518cdf68fa875061e0d954edfb2500b50b30")

    depends_on("mummer", type=("build", "run"))
