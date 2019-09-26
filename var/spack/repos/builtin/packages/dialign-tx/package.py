# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DialignTx(MakefilePackage):
    """DIALIGN-TX: greedy and progressive approaches for segment-based
       multiple sequence alignment"""

    homepage = "http://dialign-tx.gobics.de/"
    url      = "http://dialign-tx.gobics.de/DIALIGN-TX_1.0.2.tar.gz"

    version('1.0.2', '8ccfb1d91136157324d1e513f184ca29')

    build_directory = 'source'

    conflicts('%gcc@6:')

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter(' -march=i686 ', ' ')
            makefile.filter('CC=gcc', 'CC=%s' % spack_cc)
            if spec.target.family == 'aarch64':
                makefile.filter('-mfpmath=sse -msse  -mmmx', ' ')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('dialign-tx', prefix.bin)
            # t-coffee recognizes as dialign-t
            install('dialign-tx', join_path(prefix.bin, 'dialign-t'))
