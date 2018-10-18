# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
