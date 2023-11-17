# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class GoScc(GoPackage):
    """
    Sloc, Cloc and Code: scc is a very fast accurate code counter with
    complexity calculations and COCOMO estimates written in pure Go.
    """

    homepage = "https://github.com/boyter/scc"
    url = "https://github.com/boyter/scc/archive/refs/tags/v3.1.0.tar.gz"
    git = "https://github.com/boyter/scc.git"

    version("master", branch="master")
    version("3.1.0", sha256="bffea99c7f178bc48bfba3c64397d53a20a751dfc78221d347aabdce3422fd20")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("scc", prefix.bin)
