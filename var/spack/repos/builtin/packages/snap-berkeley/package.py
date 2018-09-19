##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class SnapBerkeley(MakefilePackage):
    """SNAP is a fast and accurate aligner for short DNA reads. It is
       optimized for modern read lengths of 100 bases or higher, and takes
       advantage of these reads to align data quickly through a hash-based
       indexing scheme."""

    homepage = "http://snap.cs.berkeley.edu/"
    url      = "https://github.com/amplab/snap/archive/v1.0beta.18.tar.gz"

    version('1.0beta.18', '41e595fffa482e9eda1c3f69fb5dedeb')
    version('0.15',       'a7d87cc822f052665a347ab0aa84d4de', preferred=True)

    depends_on('zlib')

    conflicts('%gcc@6:')
    conflicts('%cce')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if self.spec.satisfies('@1.0beta.18:'):
            install('snap-aligner', prefix.bin)
            install('SNAPCommand', prefix.bin)
        else:
            install('snap', prefix.bin)
