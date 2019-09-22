# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Maker(Package):
    """MAKER is a portable and easily configurable genome annotation pipeline.
    It's purpose is to allow smaller eukaryotic and prokaryotic genomeprojects
    to independently annotate their genomes and to create genome databases.
    MAKER identifies repeats, aligns ESTs and proteins to a genome, produces
    ab-initio gene predictions and automatically synthesizes these data into
    gene annotations having evidence-based quality values. MAKER is also easily
    trainable: outputs of preliminary runs can be used to automatically retrain
    its gene prediction algorithm, producing higher quality gene-models on
    subsequent runs. MAKER's inputs are minimal and its ouputs can be directly
    loaded into a GMOD database. They can also be viewed in the Apollo genome
    browser; this feature of MAKER provides an easy means to annotate, view and
    edit individual contigs and BACs without the overhead of a database. MAKER
    should prove especially useful for emerging model organism projects with
    minimal bioinformatics expertise and computer resources.

    Note: MAKER requires registration. Fill out the form at
    http://yandell.topaz.genetics.utah.edu/cgi-bin/maker_license.cgi to get a
    download link. Spack will search your current directory for the download
    file. Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.yandell-lab.org/software/maker.html"

    version('2.31.10',      sha256='d3979af9710d61754a3b53f6682d0e2052c6c3f36be6f2df2286d2587406f07d')

    def url_for_version(self, version):
        return "file://{0}/maker-{1}.tgz".format(os.getcwd(), version)

    variant('mpi', default=True, description='Build with MPI support')

    patch('install.patch')
    patch('mpi.patch')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-module-build', type='build')
    depends_on('perl-dbi', type=('build', 'run'))
    depends_on('perl-dbd-pg', type=('build', 'run'))
    depends_on('perl-dbd-sqlite', type=('build', 'run'))
    depends_on('perl-forks', type=('build', 'run'))
    depends_on('perl-file-which', type=('build', 'run'))
    depends_on('perl-perl-unsafe-signals', type=('build', 'run'))
    depends_on('perl-bit-vector', type=('build', 'run'))
    depends_on('perl-inline-c', type=('build', 'run'))
    depends_on('perl-io-all', type=('build', 'run'))
    depends_on('perl-io-prompt', type=('build', 'run'))
    depends_on('perl-bioperl', type=('build', 'run'))
    depends_on('blast-plus')
    depends_on('snap-korf')
    depends_on('repeatmasker')
    depends_on('exonerate')
    depends_on('augustus')
    depends_on('interproscan@:4.8')
    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
        if '+mpi' in spec:
            with working_dir('src'):
                pattern = r'my \$go = 0;'
                repl = 'my $go = 1;'
                filter_file(pattern, repl, 'Build.PL', backup=False)

        perl = which('perl')
        with working_dir('src'):
            perl('Build.PL', '--install_base', prefix)
            perl('Build', 'install')

    def setup_environment(self, spack_env, run_env):
        run_env.set('ZOE', join_path(self.spec['snap-korf'].prefix, 'Zoe'))
