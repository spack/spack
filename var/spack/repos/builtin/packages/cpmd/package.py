# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil


class Cpmd(MakefilePackage):
    """The CPMD code is a parallelized plane wave / pseudopotential
    implementation of Density Functional Theory, particularly
    designed for ab-initio molecular dynamics."""

    homepage = "https://www.cpmd.org/wordpress/"
    url = "file://{0}/cpmd-v4.3.tar.gz".format(os.getcwd())

    version(
        '4.3', sha256='4f31ddf045f1ae5d6f25559d85ddbdab4d7a6200362849df833632976d095df4')

    # Patch to ver4624
    patch('cpmd_4624.patch', when='@4.3')

    variant('omp', description='Enables the use of OMP instructions',
            default=False)
    variant('mpi', description='Build with MPI support', default=False)

    depends_on('lapack')
    depends_on('mpi', when='+mpi')

    conflicts('^openblas threads=none', when='+omp')
    conflicts('^openblas threads=pthreads', when='+omp')

    def edit(self, spec, prefix):
        # patch configure file
        cbase = 'LINUX-GFORTRAN'
        cp = join_path('configure', cbase)
        # Compilers
        if spec.satisfies('+mpi'):
            filter_file(
                'FC=.+',
                'FC=\'{0}\''.format(spec["mpi"].mpifc),
                cp
            )
            filter_file(
                'CC=.+',
                'CC=\'{0}\''.format(spec["mpi"].mpicc),
                cp
            )
            filter_file(
                'LD=.+',
                'LD=\'{0}\''.format(spec["mpi"].mpifc),
                cp
            )
        else:
            filter_file(
                'FC=.+',
                'FC=\'{0}\''.format(spack_fc),
                cp
            )
            filter_file(
                'CC=.+',
                'CC=\'{0}\''.format(spack_cc),
                cp
            )
            filter_file(
                'LD=.+',
                'LD=\'{0}\''.format(spack_fc),
                cp
            )

        # MPI flag
        if spec.satisfies('+mpi'):
            filter_file('-D__Linux', '-D__Linux -D__PARALLEL', cp)

        # lapack
        filter_file(
            'LIBS=.+',
            'LIBS=\'{0}\''.format(spec['lapack'].libs.ld_flags),
            cp
        )

        # LIBS:remove -static
        if spec.satisfies('%fj') and spec.satisfies('+omp'):
            filter_file(
                '\'-static \'',
                '\'-Nlibomp \'',
                cp
            )
        else:
            filter_file(
                '\'-static \'',
                '',
                cp
            )
        # Non-gcc
        # fj
        if spec.satisfies('%fj'):
            filter_file(
                '-ffixed-form',
                '-Fixed',
                cp
            )
            filter_file(
                '-ffree-line-length-none -falign-commons',
                '-Kalign_commons',
                cp
            )
            filter_file(
                '-fopenmp',
                '-Kopenmp',
                cp
            )

        # create Makefile
        bash = which('bash')
        if spec.satisfies('+omp'):
            bash('./configure.sh', '-omp', cbase)
        else:
            bash('./configure.sh', cbase)

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def test_h2o(self):
        tpath = join_path(os.path.dirname(__file__), "test")
        tfile = join_path(tpath, '1-h2o-pbc-geoopt.inp')
        cpmdexe = Executable(join_path('bin', 'cpmd.x'))
        cpmdexe(tfile, tpath)

    def install(self, spec, prefix):
        install_tree('.', prefix)
