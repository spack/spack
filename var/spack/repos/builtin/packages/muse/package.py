# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Muse(MakefilePackage):
    """Somatic point mutation caller."""

    homepage = "http://bioinformatics.mdanderson.org/main/MuSE"
    url      = "https://github.com/danielfan/MuSE/archive/v1.0-rc.tar.gz"

    version('1.0-rc', 'c63fdb48c041f6f9545879f1a7e4da58')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('MuSE', prefix.bin.MuSE)
