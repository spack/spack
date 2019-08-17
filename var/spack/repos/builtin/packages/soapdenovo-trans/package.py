# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SoapdenovoTrans(MakefilePackage):
    """SOAPdenovo-Trans is a de novo transcriptome assembler basing on the
       SOAPdenovo framework, adapt to alternative splicing and different
       expression level among transcripts."""

    homepage = "http://soap.genomics.org.cn/SOAPdenovo-Trans.html"
    url      = "https://github.com/aquaskyline/SOAPdenovo-Trans/archive/1.0.4.tar.gz"

    version('1.0.4', 'a3b00b0f743b96141c4d5f1b49f2918c')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('CFLAGS=         -O3 -fomit-frame-pointer -static',
                            'CFLAGS=         -O3 -fomit-frame-pointer')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            make('127mer=1', parallel=False)

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
