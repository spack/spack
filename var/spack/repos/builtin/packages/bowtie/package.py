# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bowtie(MakefilePackage):
    """Bowtie is an ultrafast, memory-efficient short read aligner
    for short DNA sequences (reads) from next-gen sequencers."""

    homepage = "https://sourceforge.net/projects/bowtie-bio/"
    url      = "https://github.com/BenLangmead/bowtie/archive/v1.2.0.tar.gz"

    # Release 1.2.2 fails to build with gcc@8.2.0
    # Note that release 1.2.2 is tagged as v1.2.2_p1, so the URL is "odd".
    version('1.2.2', sha256='e1b02b2e77a0d44a3dd411209fa1f44f0c4ee304ef5cc83f098275085740d5a1', url="https://github.com/BenLangmead/bowtie/archive/v1.2.2_p1.tar.gz")
    version('1.2.1.1', sha256='1b38408b88f61d18d7ff28b2470a8cfeefccb3fc59fd46e4cc62e23874e52c20')
    version('1.2.1', sha256='b2a7c8c879cb08f00a82665bee43e1d4861de44a87912c54d168e44c90869728')
    version('1.2.0', sha256='dc4e7951b8eca56ce7714c47fd4e84f72badd5312ee9546c912af1963570f894')
    version('1.2', md5='6d97f0ea1a65af11d17cc270cfac4af9', url='https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.0/bowtie-1.2-source.zip')

    # Feel free to tighten this.  I know that
    # - 1.2 -> 1.2.2 work with %gcc@5.5.0;
    # - 1.2 -> 1.2.1.1 work with %gcc@8.2.0; and
    # - 1.2.2 fails with %gcc@8.2.0
    conflicts('%gcc@6.0.0:', when='@1.2.2')

    variant('tbb', default=False, description='Use Intel thread building block')

    depends_on('tbb', when='+tbb')

    # See: https://github.com/BenLangmead/bowtie/issues/87, a
    # different fix is in the FreeBSD ports/package tree
    # https://svnweb.freebsd.org/ports?view=revision&revision=483954
    patch('issue-87.patch', when='%gcc@8.0.0:')

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
