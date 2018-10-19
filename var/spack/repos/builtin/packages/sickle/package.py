# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sickle(MakefilePackage):
    """Sickle is a tool that uses sliding windows along with quality and
       length thresholds to determine when quality is sufficiently low to trim
       the 3'-end of reads and also determines when the quality is
       sufficiently high enough to trim the 5'-end of reads."""

    homepage = "https://github.com/najoshi/sickle"
    url      = "https://github.com/najoshi/sickle/archive/v1.33.tar.gz"

    version('1.33', '9e2ba812183e1515198c9e15c4cd2cd7')

    depends_on('zlib')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('sickle', prefix.bin)
