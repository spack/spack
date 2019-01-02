# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bowtie(MakefilePackage):
    """Bowtie is an ultrafast, memory-efficient short read aligner
    for short DNA sequences (reads) from next-gen sequencers."""

    homepage = "https://sourceforge.net/projects/bowtie-bio/"
    url      = "https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.0/bowtie-1.2-source.zip"

    version('1.2', '6d97f0ea1a65af11d17cc270cfac4af9')

    variant('tbb', default=False, description='Use Intel thread building block')

    depends_on('tbb', when='+tbb')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('CC = .*', 'CC = ' + env['CC'])
        makefile.filter('CXX = .*', 'CPP = ' + env['CXX'])

    def build(self, spec, prefix):
        if '+tbb' in spec:
            make()
        else:
            make('NO_TBB=1')

    def install(self, spec, prefix):
        make('prefix={0}'.format(self.prefix), 'install')
