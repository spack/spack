# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mafft(Package):
    """MAFFT is a multiple sequence alignment program for unix-like
       operating systems.  It offers a range of multiple alignment
       methods, L-INS-i (accurate; for alignment of <~200 sequences),
       FFT-NS-2 (fast; for alignment of <~30,000 sequences), etc."""

    homepage = "http://mafft.cbrc.jp/alignment/software/index.html"
    url      = "http://mafft.cbrc.jp/alignment/software/mafft-7.221-with-extensions-src.tgz"

    version('7.221', 'b1aad911e51024d631722a2e061ba215')

    def install(self, spec, prefix):
        with working_dir('core'):
            make('PREFIX=%s' % prefix)
            make('PREFIX=%s' % prefix, 'install')
