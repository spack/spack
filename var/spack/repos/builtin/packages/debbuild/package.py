# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Debbuild(AutotoolsPackage):
    """Build deb packages from rpm specifications."""

    homepage = "https://github.com/debbuild/debbuild"
    url      = "https://github.com/debbuild/debbuild/archive/20.04.0.tar.gz"

    version('21.01.0', sha256='13278814618c8ec7f6377ed013895259f6a94bf50144ba2878342db5bb6799da')
    version('20.12.1', sha256='451c91741b31f442482bd240f2aa000a2b73691594a4b687582c5e084f828d3b')
    version('20.12.0', sha256='ae3c3af3e2dbe683a7afad4200a4d5307e2abeeff7090fc013ccd6d4d97813ac')
    version('20.04.0', sha256='e17c4f5b37e8c16592ebd99281884cabc053fb890af26531e9825417047d1430')
