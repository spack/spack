# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Cpmd(MakefilePackage):
    """The CPMD code is a parallelized plane wave / pseudopotential
    implementation of Density Functional Theory, particularly
    designed for ab-initio molecular dynamics."""

    homepage = "https://www.cpmd.org/wordpress/"
    url = "file://{0}/cpmd-v4.3.tar.gz".format(os.getcwd())

    version('4.3', sha256='4f31ddf045f1ae5d6f25559d85ddbdab4d7a6200362849df833632976d095df4')

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
        cp = FileFilter(join_path('configure', cbase))
        # Compilers
        if spec.satisfies('+mpi'):
            fc = spec["mpi"].mpifc
            cc = spec["mpi"].mpicc
        else:
            fc = spack_fc
            cc = spack_cc

        cp.filter('FC=.+', 'FC=\'{0}\''.format(fc))
        cp.filter('CC=.+', 'CC=\'{0}\''.format(cc))
        cp.filter('LD=.+', 'LD=\'{0}\''.format(fc))

        # MPI flag
        if spec.satisfies('+mpi'):
            cp.filter('-D__Linux', '-D__Linux -D__PARALLEL')

        # OMP flag
        if spec.satisfies('+omp'):
            cp.filter('-fopenmp', self.compiler.openmp_flag)

        # lapack
        cp.filter(
            'LIBS=.+',
            'LIBS=\'{0}\''.format(spec['lapack'].libs.ld_flags)
        )

        # LFLAGS
        cp.filter('\'-static \'', '')

        # Compiler specific
        if spec.satisfies('%fj'):
            cp.filter('-ffixed-form', '-Fixed')
            cp.filter('-ffree-line-length-none', '')
            cp.filter('-falign-commons', '-Kalign_commons')
            if spec.satisfies('+omp'):
                cp.filter('LFLAGS=\$', 'LFLAGS=\'-Nlibomp \'$')

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
        if self.spec.satisfies('+mpi'):
            mpirun = os.getenv('MPIRUN')
            if mpirun is None:
                mpirun = 'mpirun'
            mpipath = os.path.join(self.spec['mpi'].prefix.bin, mpirun)
            if not os.path.exists(mpipath):
                raise InstallError('mpirun not found; define MPIRUN env.')
            mpiexec = Executable(mpipath)
            mpiexec('-n', '2', join_path('bin', 'cpmd.x'), tfile, tpath)
        else:
            cpmdexe = Executable(join_path('bin', 'cpmd.x'))
            cpmdexe(tfile, tpath)

    def install(self, spec, prefix):
        install_tree('.', prefix)
