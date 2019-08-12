# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.compiler import UnsupportedCompilerFlag


class Warpx(MakefilePackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.
    """

    homepage = "https://ecp-warpx.github.io/index.html"
    url      = "https://github.com/ECP-WarpX/WarpX"

    version('master', git='https://github.com/ECP-WarpX/WarpX.git', tag='master')
    version('dev', git='https://github.com/ECP-WarpX/WarpX.git', tag='dev')

    depends_on('mpi')

    variant('dims',
            default='3',
            values=('1', '2', '3'),
            multi=False,
            description='Number of spatial dimensions')

    variant('psatd', default=False, description='Enable PSATD solver')
    variant('do_electrostatic', default=False, description='Include electrostatic solver')
    variant('debug', default=False, description='Enable debugging features')
    variant('tprof', default=False, description='Enable tiny profiling features')
    variant('openmp', default=True, description='Enable OpenMP features')

    depends_on('fftw@3:', when='+psatd')

    resource(name='amrex',
             git='https://github.com/AMReX-Codes/amrex.git',
             when='@master',
             tag='master')

    resource(name='amrex',
             git='https://github.com/AMReX-Codes/amrex.git',
             when='@dev',
             tag='development')

    resource(name='picsar',
             git='https://bitbucket.org/berkeleylab/picsar.git',
             tag='master')

    @property
    def build_targets(self):
        if self.spec.satisfies('%clang'):
            return ['CXXFLAGS={0}'.format(self.compiler.cxx11_flag)]
        else:
            return []

    def edit(self, spec, prefix):

        comp = 'gcc'
        vendors = {'%gcc': 'gcc', '%intel': 'intel'}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                comp = value

        def torf(s):
            "Returns the string TRUE or FALSE"
            return repr(s in spec).upper()

        makefile = FileFilter('GNUmakefile')
        makefile.filter('AMREX_HOME .*', 'AMREX_HOME = amrex')
        makefile.filter('PICSAR_HOME .*', 'PICSAR_HOME = picsar')
        makefile.filter('COMP .*', 'COMP = {0}'.format(comp))
        makefile.filter('DIM .*',
                        'DIM = {0}'.format(int(spec.variants['dims'].value)))
        makefile.filter('USE_PSATD .*',
                        'USE_PSATD = {0}'.format(torf('+psatd')))
        makefile.filter('DO_ELECTROSTATIC .*',
                        'DO_ELECTROSTATIC = %s' % torf('+do_electrostatic'))
        try:
            self.compiler.openmp_flag
        except UnsupportedCompilerFlag:
            use_omp = 'FALSE'
        else:
            use_omp = torf('+openmp')
        makefile.filter('USE_OMP .*',
                        'USE_OMP = {0}'.format(use_omp))
        makefile.filter('DEBUG .*',
                        'DEBUG = {0}'.format(torf('+debug')))
        makefile.filter('TINY_PROFILE .*',
                        'TINY_PROFILE = {0}'.format(torf('+tprof')))
        makefile.filter('EBASE .*', 'EBASE = warpx')

    def setup_environment(self, spack_env, run_env):
        # --- Fool the compiler into using the "unknown" configuration.
        # --- With this, it will use the spack provided mpi.
        spack_env.set('HOSTNAME', 'unknown')
        spack_env.set('NERSC_HOST', 'unknown')

    def install(self, spec, prefix):
        make('WarpxBinDir = {0}'.format(prefix.bin), 'all')
