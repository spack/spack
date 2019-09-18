# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob


class Braker(Package):
    """BRAKER is a pipeline for unsupervised RNA-Seq-based genome annotation
       that combines the advantages of GeneMark-ET and AUGUSTUS"""

    homepage = "http://exon.gatech.edu/braker1.html"
    url      = "https://github.com/Gaius-Augustus/BRAKER/archive/v2.1.4.tar.gz"
    list_url = "http://bioinf.uni-greifswald.de/augustus/binaries/old"

    version('2.1.4', sha256='d48af5649cc879343046f9ddf180fe2c709b5810e0b78cf314bf298514d31d52')
    version('2.1.0', '5f974abcceb9f96a11668fa20a6f6a56')
    version('1.11', '297efe4cabdd239b710ac2c45d81f6a5',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/BRAKER1_v1.11.tar.gz')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-scalar-util-numeric', type=('build', 'run'))
    depends_on('perl-parallel-forkmanager', type=('build', 'run'))
    depends_on('perl-file-which', type=('build', 'run'))
    depends_on('perl-yaml', type=('build', 'run'))
    depends_on('perl-hash-merge', type=('build', 'run'))
    depends_on('perl-logger-simple', type=('build', 'run'))
    depends_on('perl-file-homedir', when='@2.1.4:', type=('build', 'run'))
    depends_on('augustus')
    depends_on('augustus@3.2.3', when='@:2.1.0')
    depends_on('genemark-et')
    depends_on('bamtools')
    depends_on('samtools')
    depends_on('diamond')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        if self.version < Version('2.1.2'):
            install('braker.pl', prefix.bin)
            install('filterGenemark.pl', prefix.bin)
            install('filterIntronsFindStrand.pl', prefix.bin)
            install('helpMod.pm', prefix.lib)
        else:
            install_tree('docs', prefix.docs)
            install_tree('example', prefix.example)
            with working_dir('scripts'):
                install('helpMod.pm', prefix.lib)
                files = glob.iglob('*.pl')
                for file in files:
                    if os.path.isfile(file):
                        install(file, prefix.bin)

    @run_after('install')
    def filter_sbang(self):
        with working_dir(self.prefix.bin):
            pattern = '^#!.*/usr/bin/env perl'
            repl = '#!{0}'.format(self.spec['perl'].command.path)
            files = glob.iglob("*.pl")
            for file in files:
                filter_file(pattern, repl, *files, backup=False)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix.lib)
