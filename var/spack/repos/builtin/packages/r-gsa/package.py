# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGsa(RPackage):
    """Gene Set Analysis."""

    cran = "GSA"

    version('1.03.1', sha256='e192d4383f53680dbd556223ea5f8cad6bae62a80a337ba5fd8d05a8aee6a917')
