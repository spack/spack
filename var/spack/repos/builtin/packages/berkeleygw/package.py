# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Berkeleygw(MakefilePackage):
    """BerkeleyGW is a many-body perturbation theory code for excited states,
    using the GW method and the GW plus Bethe-Salpeter equation (GW-BSE) method
    to solve respectively for quasiparticle excitations and optical properties of
    materials."""

    homepage = "https://berkeleygw.org"

    version('2.1',
            '31f3b643dd937350c3866338321d675d4a1b1f54c730b43ad74ae67e75a9e6f2',
            url='https://berkeley.box.com/shared/static/ze3azi5vlyw7hpwvl9i5f82kaiid6g0x.gz',
            expand=False)

    variant('elpa', default=True, description='Build with ELPA support')
    variant('openmp', default=True, description='Build with OpenMP support')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')

    depends_on('fftw+openmp', when='+openmp')
    depends_on('fftw~openmp', when='~openmp')

    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')

    depends_on('hdf5+fortran+hl')

    depends_on('py-h5py', type=('build', 'run'))

    depends_on('perl', type='test')

    parallel = False

    def edit(self, spec, prefix):
        # archive is a tar file, despite the .gz expension
        os.system("tar xf %s --strip-components=1" % self.stage.archive_file)

        # get generic arch.mk template
        copy(os.path.join(os.getcwd(), 'config', 'generic.mpi.linux.mk'), 'arch.mk')

        # don't try to install missing file
        filter_file('install manual.html', '#install manual.html', 'Makefile')

        # use parallelization in tests
        filter_file(r'cd testsuite \&\& \$\(MAKE\) check$',
                    'cd testsuite && $(MAKE) check-parallel',
                    'Makefile')

        # remove stack ulimit in order to run openmp tests
        filter_file(r'function run_testsuite\(\) {',
                    'function run_testsuite() {\nulimit -s unlimited',
                    'testsuite/run_testsuite.sh')

    def setup_build_environment(self, env):
        if self.run_tests:
            env.set('OMP_NUM_THREADS', '2')
            env.set('BGW_TEST_MPI_NPROCS', '2')

    def build(self, spec, prefix):

        buildopts = []
        paraflags = []

        paraflags.append('-DMPI')

        if '+openmp' in spec:
            paraflags.append('-DOMP')
            spec.compiler_flags['fflags'].append(self.compiler.openmp_flag)

        buildopts.append('C_PARAFLAG=-DPARA')
        buildopts.append('PARAFLAG=%s' % ' '.join(paraflags))

        if '+debug' in spec:
            buildopts.append('DEBUGFLAG=-DDEBUG -DVERBOSE')
        else:
            buildopts.append('DEBUGFLAG=')

        buildopts.append('LINK=%s' % spec['mpi'].mpifc)
        buildopts.append('C_LINK=%s' % spec['mpi'].mpicxx)

        buildopts.append('FOPTS=%s' % ' '.join(spec.compiler_flags['fflags']))
        buildopts.append('C_OPTS=%s' % ' '.join(spec.compiler_flags['cflags']))

        mathflags = []
        mathflags.append('-DUSEFFTW3')
        buildopts.append('FFTWINCLUDE=%s' % spec['fftw'].prefix.include)
        fftwlibs = '-lfftw3 -lfftw3f'
        if '+openmp' in spec:
            fftwlibs = '-lfftw3_omp ' + fftwlibs
        buildopts.append('FFTWLIB=-L%s %s' % (spec['fftw'].libs, fftwlibs))

        mathflags.append('-DUSESCALAPACK')
        buildopts.append('LAPACKLIB=%s' % spec['lapack'].libs.ld_flags)
        buildopts.append('SCALAPACKLIB=%s' % spec['scalapack'].libs.ld_flags)

        if spec.satisfies('%intel'):
            buildopts.append('COMPFLAG=-DINTEL')
            buildopts.append('MOD_OPT=-module ')
            buildopts.append('F90free=%s -free' % spec['mpi'].mpifc)
            buildopts.append('FCPP=cpp -C -P -ffreestanding')
            buildopts.append('C_COMP=%s' % spec['mpi'].mpicc)
            buildopts.append('CC_COMP=%s' % spec['mpi'].mpicxx)
            buildopts.append('BLACSDIR=%s' % spec['scalapack'].libs)
            buildopts.append('BLACS=%s' % spec['scalapack'].libs.ld_flags)
        elif spec.satisfies('%gcc'):
            c_flags = '-std=c99'
            cxx_flags = '-std=c++0x'
            f90_flags = "-ffree-form -ffree-line-length-none -fno-second-underscore"
            if spec.satisfies('%gcc@10:'):
                c_flags += ' -fcommon'
                cxx_flags += ' -fcommon'
                f90_flags += ' -fallow-argument-mismatch'
            buildopts.append('COMPFLAG=-DGNU')
            buildopts.append('MOD_OPT=-J ')
            buildopts.append('F90free=%s %s' % (spec['mpi'].mpifc, f90_flags))
            buildopts.append('FCPP=cpp -C -nostdinc')
            buildopts.append('C_COMP=%s %s' % (spec['mpi'].mpicc, c_flags))
            buildopts.append('CC_COMP=%s %s' % (spec['mpi'].mpicxx, cxx_flags))
        else:
            raise InstallError("Spack does not yet have support for building "
                               "BerkeleyGW with compiler %s" % spec.compiler)

        mathflags.append('-DHDF5')
        buildopts.append('HDF5INCLUDE=%s' % spec['hdf5'].prefix.include)
        buildopts.append('HDF5LIB=%s' % spec['hdf5:hl,fortran'].libs.ld_flags)

        if '+elpa' in spec:
            mathflags.append('-DUSEELPA')
            elpa = spec['elpa']

            if '+openmp' in spec:
                elpa_suffix = '_openmp'
            else:
                elpa_suffix = ''

            elpa_incdir = elpa.headers.directories[0]
            elpa_libs = os.path.join(elpa.libs.directories[0],
                                     'libelpa%s.%s' % (elpa_suffix, dso_suffix))

            buildopts.append('ELPALIB=%s' % elpa_libs)
            buildopts.append('ELPAINCLUDE=%s' % os.path.join(elpa_incdir, 'modules'))

        buildopts.append('MATHFLAG=%s' % ' '.join(mathflags))

        make('all-flavors', *buildopts)

    def install(self, spec, prefix):
        make('install', 'INSTDIR=%s' % prefix)
