# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Primer3(MakefilePackage):
    """Primer3 is a widely used program for designing PCR primers
       (PCR = "Polymerase Chain Reaction"). PCR is an essential and
       ubiquitous tool in genetics and molecular biology. Primer3
       can also design hybridization probes and sequencing primers."""

    homepage = "http://primer3.sourceforge.net/"
    url      = "https://sourceforge.net/projects/primer3/files/primer3/2.3.7/primer3-2.3.7.tar.gz/download"

    version('2.3.7', 'c6b89067bf465e62b6b1fd830b5b4418')

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            for binary in ('primer3_core', 'ntdpal', 'oligotm',
                           'long_seq_tm_test'):
                install(binary, prefix.bin)
