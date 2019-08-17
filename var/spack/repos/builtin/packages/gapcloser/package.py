# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gapcloser(Package):
    """The GapCloser is designed to close the gaps emerging during the
       scaffolding process"""

    homepage = "https://sourceforge.net/projects/soapdenovo2/files/GapCloser/"
    url      = "https://downloads.sourceforge.net/project/soapdenovo2/GapCloser/bin/r6/GapCloser-bin-v1.12-r6.tgz"

    version('1.12-r6', '42b4e4256bdc9f9f31a391a359256209')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('GapCloser', prefix.bin)
