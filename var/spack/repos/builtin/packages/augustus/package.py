# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Augustus(MakefilePackage):
    """AUGUSTUS is a program that predicts genes in eukaryotic
       genomic sequences"""

    homepage = "http://bioinf.uni-greifswald.de/augustus/"
    url      = "https://github.com/Gaius-Augustus/Augustus/archive/3.3.2.tar.gz"
    # Releases have moved to github

    version('3.3.2', sha256='d09f972cfd88deb34b19b69878eb8af3bbbe4f1cde1434b69cedc2aa6247a0f2')
    version('3.3.1', sha256='011379606f381ee21b9716f83e8a1a57b2aaa01aefeebd2748104efa08c47cab',
            url='https://github.com/Gaius-Augustus/Augustus/archive/v3.3.1-tag1.tar.gz')
    version('3.3',   '93691d9aafc7d3d0e1adf31ec308507f',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/augustus-3.3.tar.gz')
    version('3.2.3', 'b8c47ea8d0c45aa7bb9a82626c8ff830',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/augustus-3.2.3.tar.gz')

    depends_on('perl', type=('build', 'run'))
    depends_on('bamtools')
    depends_on('gsl')
    depends_on('boost')
    depends_on('zlib')
    depends_on('htslib', when='@3.3.1:')
    depends_on('bcftools', when='@3.3.1:')
    depends_on('samtools', when='@3.3.1:')
    depends_on('curl', when='@3.3.1:')

    def edit(self, spec, prefix):
        with working_dir(join_path('auxprogs', 'filterBam', 'src')):
            makefile = FileFilter('Makefile')
            makefile.filter('BAMTOOLS = .*', 'BAMTOOLS = %s' % self.spec[
                            'bamtools'].prefix)
            makefile.filter('INCLUDES = *',
                            'INCLUDES = -I$(BAMTOOLS)/include/bamtools ')
            if 'bamtools@2.5:' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib64/'
                                '/libbamtools.a -lz')
            if 'bamtools@:2.4' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib/bamtools'
                                '/libbamtools.a -lz')
        with working_dir(join_path('auxprogs', 'bam2hints')):
            makefile = FileFilter('Makefile')
            makefile.filter('# Variable definition',
                            'BAMTOOLS = %s' % self.spec['bamtools'].prefix)
            makefile.filter('INCLUDES = /usr/include/bamtools',
                            'INCLUDES = $(BAMTOOLS)/include/bamtools')
            if 'bamtools@2.5:' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib64/'
                                '/libbamtools.a -lz')
            if 'bamtools@:2.4' in spec:
                makefile.filter('LIBS = -lbamtools -lz',
                                'LIBS = $(BAMTOOLS)/lib/bamtools'
                                '/libbamtools.a -lz')
        with working_dir(join_path('auxprogs', 'bam2wig')):
            makefile = FileFilter('Makefile')
            # point tools to spack installations
            if 'bcftools' in spec:
                bcftools = self.spec['bcftools'].prefix.include
                makefile.filter('BCFTOOLS=.*$',
                                'BCFTOOLS=%s' % bcftools)
            if 'samtools' in spec:
                samtools = self.spec['samtools'].prefix.include
                makefile.filter('SAMTOOLS=.*$',
                                'SAMTOOLS=%s' % samtools)
            if 'htslib' in spec:
                htslib = self.spec['htslib'].prefix.include
                makefile.filter('HTSLIB=.*$',
                                'HTSLIB=%s' % htslib)

            # fix bad linking dirs
            makefile.filter('$(SAMTOOLS)/libbam.a',
                            '$(SAMTOOLS)/../lib/libbam.a', string=True)
            makefile.filter('$(HTSLIB)/libhts.a',
                            '$(HTSLIB)/../lib/libhts.a', string=True)

    def install(self, spec, prefix):
        install_tree('bin', join_path(self.spec.prefix, 'bin'))
        install_tree('config', join_path(self.spec.prefix, 'config'))
        install_tree('scripts', join_path(self.spec.prefix, 'scripts'))

    @run_after('install')
    def filter_sbang(self):
        with working_dir(self.prefix.scripts):
            pattern = '^#!.*/usr/bin/perl'
            repl = '#!{0}'.format(self.spec['perl'].command.path)
            files = glob.iglob("*.pl")
            for file in files:
                filter_file(pattern, repl, *files, backup=False)

    def setup_environment(self, spack_env, run_env):
        run_env.set('AUGUSTUS_CONFIG_PATH', join_path(
            self.prefix, 'config'))
        run_env.prepend_path('PATH', join_path(self.prefix, 'scripts'))
