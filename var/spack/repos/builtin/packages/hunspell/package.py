# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hunspell(AutotoolsPackage):
    """The most popular spellchecking library (sez the author...)."""

    homepage = "http://hunspell.github.io/"
    url      = "https://github.com/hunspell/hunspell/archive/v1.6.0.tar.gz"

    version('1.6.0', '047c3feb121261b76dc16cdb62f54483')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
