# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Samblaster(MakefilePackage):
    """A tool to mark duplicates and extract discordant and split reads from
    sam files."""

    homepage = "https://github.com/GregoryFaust/samblaster"
    url      = "https://github.com/GregoryFaust/samblaster/archive/v.0.1.24.tar.gz"

    version('0.1.24', '885d5782cc277865dfb086fc0a20243e')
    version('0.1.23', '95d33b6fcceaa38a9bd79014446b4545')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('samblaster', prefix.bin)
