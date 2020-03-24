# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    git      = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers = ['ax3l', 'dpgrote', 'MaxThevenet', 'RemiLehe']

    version('master', tag='master')

    variant('dims',
            default='3',
            values=('2', '3'),
            multi=False,
            description='Number of spatial dimensions')

    variant('psatd', default=False, description='Enable PSATD solver')
    variant('debug', default=False, description='Enable debugging features')
    variant('tprof', default=True, description='Enable tiny profiling features')
    variant('openmp', default=True, description='Enable OpenMP features')
    variant('openpmd', default=True, description='Enable openPMD I/O')

    depends_on('mpi')
    depends_on('fftw@3:', when='+psatd')
    depends_on('pkgconfig', type='build', when='+openpmd')
    depends_on('python', type='build')  # FIXME upstream
    depends_on('openpmd-api@0.11.0:,dev +mpi', when='+openpmd')

    resource(name='amrex',
             git='https://github.com/AMReX-Codes/amrex.git',
             when='@master',
             tag='development')

    resource(name='picsar',
             git='https://bitbucket.org/berkeleylab/picsar.git',
             tag='master')

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
        try:
            self.compiler.openmp_flag
        except UnsupportedCompilerFlag:
            use_omp = 'FALSE'
        else:
            use_omp = torf('+openmp')
        use_openpmd = torf('+openpmd')
        makefile.filter('USE_OMP .*',
                        'USE_OMP = {0}'.format(use_omp))
        makefile.filter('USE_OPENPMD .*',
                        'USE_OPENPMD = {0}'.format(use_openpmd))
        makefile.filter('DEBUG .*',
                        'DEBUG = {0}'.format(torf('+debug')))
        makefile.filter('TINY_PROFILE .*',
                        'TINY_PROFILE = {0}'.format(torf('+tprof')))
        makefile.filter('EBASE .*', 'EBASE = warpx')

    def setup_build_environment(self, env):
        # --- Fool the compiler into using the "unknown" configuration.
        # --- With this, it will use the spack provided mpi.
        env.set('HOSTNAME', 'unknown')
        env.set('NERSC_HOST', 'unknown')

    def install(self, spec, prefix):
        make('WarpxBinDir = {0}'.format(prefix.bin), 'all')
