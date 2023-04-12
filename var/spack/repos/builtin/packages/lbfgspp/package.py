# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lbfgspp(CMakePackage):
    """A Header-only C++ Library for L-BFGS and L-BFGS-B Algorithms"""

    homepage = "https://lbfgspp.statr.me/"
    url = "https://github.com/yixuan/LBFGSpp/archive/refs/tags/v0.2.0.tar.gz"

    version("0.2.0", sha256="7101744a538c3aff52e10c82267305847b0b5e9d39f9974b4b29812cd1398ff9")

    depends_on("eigen @3:")
