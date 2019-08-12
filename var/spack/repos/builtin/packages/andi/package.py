# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Andi(AutotoolsPackage):
    """andi is used for for estimating the
    evolutionary distance between closely related genomes."""

    homepage = "https://github.com/EvolBioInf/andi"
    url      = "https://github.com/EvolBioInf/andi/archive/v0.10.tar.gz"

    version('0.10',    '3aaba7961798bb4aaa546baa44e469d8')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('gsl')
    depends_on('libdivsufsort')
