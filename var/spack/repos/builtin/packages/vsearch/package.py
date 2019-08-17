# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vsearch(AutotoolsPackage):
    """VSEARCH is a versatile open-source tool for metagenomics."""

    homepage = "https://github.com/torognes/vsearch"
    url      = "https://github.com/torognes/vsearch/archive/v2.4.3.tar.gz"

    version('2.4.3', '8f57210fe447a781078fde06e6402650')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
