##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import sys
from spack import *


class Mfem(Package):
    """Free, lightweight, scalable C++ library for finite element methods."""

    homepage = 'http://www.mfem.org'
    url      = 'https://github.com/mfem/mfem'

    maintainers = ['goxberry', 'tzanio', 'markcmiller86', 'acfisher',
                   'v-dobrev']

    # mfem is downloaded from a URL shortener at request of upstream
    # author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    #     https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new verison is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    http://mfem.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://mfem.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.

    # 'develop' is a special version that is always larger (or newer) than any
    # other version.
    version('develop',
            git='https://github.com/mfem/mfem', branch='master')

    version('3.3.2',
            '01a762a5d0a2bc59ce4e2f59009045a4',
            url='https://goo.gl/Kd7Jk8', extension='.tar.gz',
            preferred=True)

    # To properly order the 'laghos-v1.0' tagged version, we give it the version
    # number it reports (3.3.1, a development version) with the tag string
    # appended at the end.
    version('3.3.1-laghos-v1.0', git='https://github.com/mfem/mfem',
            tag='laghos-v1.0')

    version('3.3',
            'b17bd452593aada93dc0fee748fcfbbf4f04ce3e7d77fdd0341cc9103bcacd0b',
            url='http://goo.gl/Vrpsns', extension='.tar.gz')

    version('3.2',
            '2938c3deed4ec4f7fd5b5f5cfe656845282e86e2dcd477d292390058b7b94340',
            url='http://goo.gl/Y9T75B', extension='.tar.gz')

    version('3.1',
            '841ea5cf58de6fae4de0f553b0e01ebaab9cd9c67fa821e8a715666ecf18fc57',
            url='http://goo.gl/xrScXn', extension='.tar.gz')

    variant('static', default=True,
        description='Build static library')
    variant('shared', default=False,
        description='Build shared library')
    variant('mpi', default=True,
        description='Enable MPI parallelism')
    # Can we make the default value for 'metis' to depend on the 'mpi' value?
    variant('metis', default=True,
        description='Enable METIS support')
    variant('openmp', default=False,
        description='Enable OpenMP parallelism')
    variant('threadsafe', default=False,
        description=('Enable thread safe features.'
            ' Required for OpenMP.'
            ' May cause minor performance issues.'))
    variant('superlu-dist', default=False,
        description='Enable MPI parallel, sparse direct solvers')
    # Placeholder for STRUMPACK, support added in v3.3.2:
    # variant('strumpack', default=False,
    #     description='Enable support for STRUMPACK')
    variant('suite-sparse', default=False,
        description='Enable serial, sparse direct solvers')
    variant('petsc', default=False,
        description='Enable PETSc solvers, preconditioners, etc..')
    variant('sundials', default=False,
        description='Enable Sundials time integrators')
    variant('mpfr', default=False,
        description='Enable precise, 1D quadrature rules')
    variant('lapack', default=False,
        description='Use external blas/lapack routines')
    variant('debug', default=False,
        description='Build debug instead of optimized version')
    variant('netcdf', default=False,
        description='Enable Cubit/Genesis reader')
    variant('gzstream', default=True,
        description='Support zip\'d streams for I/O')
    variant('gnutls', default=False,
        description='Enable secure sockets using GnuTLS')
    variant('libunwind', default=False,
        description='Enable backtrace on error support using Libunwind')
    variant('timer', default='auto',
        values=('auto','std','posix','mac','mpi'),
        description='Timing functions to use in mfem::StopWatch')
    variant('examples', default=False,
        description='Build and install examples')
    variant('miniapps', default=False,
        description='Build and install miniapps')

    conflicts('+shared', when='@:3.3.2')
    conflicts('~static~shared')
    conflicts('~threadsafe', when='+openmp')

    conflicts('+netcdf', when='@:3.1')
    conflicts('+superlu-dist', when='@:3.1')
    conflicts('+gnutls', when='@:3.1')
    conflicts('+gzstream', when='@:3.2')
    conflicts('+mpfr', when='@:3.2')
    conflicts('+petsc', when='@:3.2')
    conflicts('+sundials', when='@:3.2')
    conflicts('timer=mac', when='@:3.3.0')
    conflicts('timer=mpi', when='@:3.3.0')
    conflicts('~metis+mpi', when='@:3.3.0')
    conflicts('+metis~mpi', when='@:3.3.0')

    conflicts('+superlu-dist', when='~mpi')
    conflicts('+petsc', when='~mpi')
    conflicts('timer=mpi', when='~mpi')

    depends_on('mpi', when='+mpi')
    depends_on('hypre', when='+mpi')
    depends_on('metis', when='+metis')
    # Avoid disabling variants:
    # depends_on('hypre~internal-superlu', when='+mpi')
    depends_on('blas', when='+lapack')
    depends_on('lapack', when='+lapack')

    depends_on('sundials@2.7.0', when='@:3.3.1+sundials~mpi')
    depends_on('sundials@2.7.0+mpi+hypre', when='@:3.3.1+sundials+mpi')
    depends_on('sundials@2.7.0:', when='@3.3.2:+sundials~mpi')
    depends_on('sundials@2.7.0:+mpi+hypre', when='@3.3.2:+sundials+mpi')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('superlu-dist', when='+superlu-dist')
    # The PETSc tests in MFEM will fail if PETSc is not configured with
    # SuiteSparse and MUMPS. On the other hand, if we require the variants
    # '+suite-sparse+mumps' of PETSc, the xsdk concretization fails.
    depends_on('petsc@3.8:+mpi+double+hypre', when='+petsc')
    # Recommended when building outside of xsdk:
    # depends_on('petsc@3.8:+mpi+double+hypre+suite-sparse+mumps', when='+petsc')
    depends_on('mpfr', when='+mpfr')
    depends_on('netcdf', when='+netcdf')
    depends_on('libunwind', when='+libunwind')
    depends_on('zlib', when='+gzstream')
    depends_on('gnutls', when='+gnutls')

    patch('mfem_ppc_build.patch', when='@3.2:3.3 arch=ppc64le')

    phases = ['configure', 'build', 'install']

    #
    # Note: Although MFEM does support CMake configuration, MFEM
    # development team indicates that vanilla GNU Make is the
    # preferred mode of configuration of MFEM and the mode most
    # likely to be up to date in supporting *all* of MFEM's
    # configuration options. So, don't use CMake
    #
    def configure(self, spec, prefix):

        def yes_no(varstr):
            return 'YES' if varstr in self.spec else 'NO'

        metis5_str = 'NO'
        if ('+metis' in spec) and spec['metis'].satisfies('@5:'):
            metis5_str = 'YES'

        options = [
            'PREFIX=%s' % prefix,
            'MFEM_USE_MEMALLOC=YES',
            'MFEM_DEBUG=%s' % yes_no('+debug'),
            'CXX=%s' % env['CXX'],
            'MFEM_USE_LIBUNWIND=%s' % yes_no('+libunwind'),
            'MFEM_USE_GZSTREAM=%s' % yes_no('+gzstream'),
            'MFEM_USE_METIS=%s' % yes_no('+metis'),
            'MFEM_USE_METIS_5=%s' % metis5_str,
            'MFEM_THREAD_SAFE=%s' % yes_no('+threadsafe'),
            'MFEM_USE_MPI=%s' % yes_no('+mpi'),
            'MFEM_USE_LAPACK=%s' % yes_no('+lapack'),
            'MFEM_USE_SUPERLU=%s' % yes_no('+superlu-dist'),
            'MFEM_USE_SUITESPARSE=%s' % yes_no('+suite-sparse'),
            'MFEM_USE_SUNDIALS=%s' % yes_no('+sundials'),
            'MFEM_USE_PETSC=%s' % yes_no('+petsc'),
            'MFEM_USE_NETCDF=%s' % yes_no('+netcdf'),
            'MFEM_USE_MPFR=%s' % yes_no('+mpfr'),
            'MFEM_USE_GNUTLS=%s' % yes_no('+gnutls'),
            'MFEM_USE_OPENMP=%s' % yes_no('+openmp')]

        if '~static' in spec:
            options += ['STATIC=NO']
        if '+shared' in spec:
            options += ['SHARED=YES', 'PICFLAG=%s' % self.compiler.pic_flag]

        if '+mpi' in spec:
            options += ['MPICXX=%s' % spec['mpi'].mpicxx]
            options += [
                'HYPRE_OPT=%s' % spec['hypre'].all_headers.cpp_flags,
                'HYPRE_LIB=%s' % spec['hypre'].all_libs.ld_flags]

        if '+metis' in spec:
            options += [
                'METIS_OPT=%s' % spec['metis'].all_headers.cpp_flags,
                'METIS_LIB=%s' % spec['metis'].all_libs.ld_flags]

        if '+lapack' in spec:
            lapack_lib = (spec['lapack'].libs + spec['blas'].libs).ld_flags  # NOQA: ignore=E501
            options += [
                # LAPACK_OPT is not used
                'LAPACK_LIB=%s' % lapack_lib]

        if '+superlu-dist' in spec:
            options += [
                'SUPERLU_OPT=%s' % spec['superlu-dist'].all_headers.cpp_flags,
                'SUPERLU_LIB=%s' % spec['superlu-dist'].all_libs.ld_flags]

        if '+suite-sparse' in spec:
            ss_spec = 'suite-sparse:' + self.suitesparse_components
            options += [
                'SUITESPARSE_OPT=%s' % spec[ss_spec].all_headers.cpp_flags,
                'SUITESPARSE_LIB=%s' % spec[ss_spec].all_libs.ld_flags]

        if '+sundials' in spec:
            sun_spec = 'sundials:' + self.sundials_components
            options += [
                'SUNDIALS_OPT=%s' % spec[sun_spec].all_headers.cpp_flags,
                'SUNDIALS_LIB=%s' % spec[sun_spec].all_libs.ld_flags]

        if '+petsc' in spec:
            options += ['PETSC_DIR=%s' % spec['petsc'].prefix]

        if '+netcdf' in spec:
            options += [
                'NETCDF_OPT=%s' % spec['netcdf'].all_headers.cpp_flags,
                'NETCDF_LIB=%s' % spec['netcdf'].all_libs.ld_flags]

        if '+gzstream' in spec:
            options += [
                'ZLIB_OPT=%s' % spec['zlib'].all_headers.cpp_flags,
                'ZLIB_LIB=%s' % spec['zlib'].all_libs.ld_flags]

        if '+mpfr' in spec:
            options += [
                'MPFR_OPT=%s' % spec['mpfr'].all_headers.cpp_flags,
                'MPFR_LIB=%s' % spec['mpfr'].all_libs.ld_flags]

        if '+gnutls' in spec:
            options += [
                'GNUTLS_OPT=%s' % spec['gnutls'].all_headers.cpp_flags,
                'GNUTLS_LIB=%s' % spec['gnutls'].all_libs.ld_flags]

        if '+libunwind' in spec:
            options += [
                'LIBUNWIND_OPT=-g %s' % spec['libunwind'].all_headers.cpp_flags,
                'LIBUNWIND_OPT=%s' % spec['libunwind'].all_libs.ld_flags]

        if '+openmp' in spec:
            options += ['OPENMP_OPT=%s' % self.compiler.openmp_flag]

        timer_ids = {'std': '0', 'posix': '2', 'mac': '4', 'mpi': '6'}
        timer = spec.variants['timer'].value
        if timer != 'auto':
            options += ['MFEM_TIMER_TYPE=%s' % timer_ids[timer]]

        make('config', *options, parallel=False)
        make('info', parallel=False)

    def build(self, spec, prefix):
        make('lib')

    @run_after('build')
    def check_or_test(self):
        # Running 'make check' or 'make test' may fail if MFEM_MPIEXEC or
        # MFEM_MPIEXEC_NP are not set appropriately.
        if not self.run_tests:
            # check we can build ex1 (~mpi) or ex1p (+mpi).
            make('-C', 'examples', 'ex1p' if ('+mpi' in self.spec) else 'ex1',
                 parallel=False)
            # make('check', parallel=False)
        else:
            make('all')
            make('test', parallel=False)

    def install(self, spec, prefix):
        make('install', parallel=False)

        # TODO: The way the examples and miniapps are being installed is not
        # perfect. For example, the makefiles do not work.

        if '+examples' in spec:
            make('examples')
            install_tree('examples', join_path(prefix, 'examples'))

        if '+miniapps' in spec:
            make('miniapps')
            install_tree('miniapps', join_path(prefix, 'miniapps'))

        if ('+examples' in spec) or ('+miniapps' in spec):
            install_tree('data', join_path(prefix, 'data'))

    @property
    def suitesparse_components(self):
        """Return the SuiteSparse components needed by MFEM."""
        ss_comps = 'umfpack,cholmod,colamd,amd,camd,ccolamd,suitesparseconfig'
        if self.spec.satisfies('@3.2:'):
            ss_comps = 'klu,btf,' + ss_comps
        return ss_comps

    @property
    def sundials_components(self):
        """Return the SUNDIALS components needed by MFEM."""
        sun_comps = 'arkode,cvode,nvecserial,kinsol'
        if '+mpi' in self.spec:
            sun_comps += ',nvecparhyp,nvecparallel'
        return sun_comps

    @property
    def headers(self):
        """Export the main mfem header, mfem.hpp.
        """
        hdrs = HeaderList(find(self.prefix.include, 'mfem.hpp',
                               recursive=False))
        return hdrs or None

    @property
    def all_headers(self):
        """Export all headers needed for compiling with mfem.
           This property can be accessed with spec['mfem'].all_headers and used
           in compilation with spec['mfem'].all_headers.cpp_flags.
        """
        spec = self.spec
        hdrs = self.headers
        # Package headers that are not needed: metis, superlu-dist, mpfr,
        # netcdf, lapack, blas, libunwind.
        pkgs = ['petsc', 'suite-sparse', 'sundials', 'gnutls']
        for pkg in pkgs:
            if '+'+pkg in spec:
                hdrs += spec[pkg].all_headers
        if '+mpi' in spec:
            hdrs += spec['hypre'].all_headers
        if '+gzstream' in spec:
            hdrs += spec['zlib'].all_headers
        return hdrs

    @property
    def libs(self):
        """Export the mfem library file.
        """
        libs = find_libraries('libmfem', root=self.prefix.lib,
                   shared=('+shared' in self.spec), recursive=False)
        return libs or None

    @property
    def all_libs(self):
        """Export all libraries that are needed when linking with mfem.
           This property can be accessed with spec['mfem'].all_libs and used for
           linking with spec['mfem'].all_libs.ld_flags.
        """
        spec = self.spec
        libs = self.libs
        if '+mpi' in spec:
            libs += spec['hypre'].all_libs
        if '+lapack' in spec:
            libs += spec['lapack'].all_libs + spec['blas'].all_libs
        pkgs = ['petsc', 'superlu-dist', 'netcdf', 'mpfr', 'gnutls',
                'libunwind', 'metis']
        for pkg in pkgs:
            if '+'+pkg in spec:
                libs += spec[pkg].all_libs
        if '+sundials' in spec:
            sun_spec = 'sundials:' + self.sundials_components
            libs += spec[sun_spec].all_libs
        if '+suite-sparse' in spec:
            ss_spec = 'suite-sparse:' + self.suitesparse_components
            libs += spec[ss_spec].all_libs
        if '+gzstream' in spec:
            libs += spec['zlib'].all_libs
        if spec.variants['timer'].value == 'posix':
            libs += find_system_libraries('librt')
        return libs

    @property
    def config_mk(self):
        """Export the location of the config.mk file.
           This property can be accessed using spec['mfem'].package.config_mk
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
           f = join_path(d, 'config.mk')
           if os.access(f, os.R_OK):
              return FileList(f)
        return FileList(find(self.prefix, 'config.mk', recursive=True))

    @property
    def test_mk(self):
        """Export the location of the test.mk file.
           This property can be accessed using spec['mfem'].package.test_mk.
           In version 3.3.2 and newer, the location of test.mk is also defined
           inside config.mk, variable MFEM_TEST_MK.
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
           f = join_path(d, 'test.mk')
           if os.access(f, os.R_OK):
              return FileList(f)
        return FileList(find(self.prefix, 'test.mk', recursive=True))
