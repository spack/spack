# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Packmol(CMakePackage):
    """Packmol creates an initial point for molecular dynamics simulations
    by packing molecules in defined regions of space."""

    homepage = "http://m3g.iqm.unicamp.br/packmol/home.shtml"
    url      = "https://github.com/mcubeg/packmol/archive/18.169.tar.gz"

    version('20.010', sha256='23285f2a9e2bef0e8253250d7eae2d4026a9535ddcc2b9b383f5ad45b19e123d')
    version('18.169', sha256='8acf2cbc742a609e763eb00cae55aecd09af2edb4cc4e931706e2f06ac380de9')
