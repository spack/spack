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
import re
from spack import *


class Mfem(Package):
    """Free, lightweight, scalable C++ library for finite element methods."""

    homepage = 'http://www.mfem.org'
    url      = 'https://github.com/mfem/mfem'

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

    version('3.3.2', 
            '01a762a5d0a2bc59ce4e2f59009045a4',
            url='https://goo.gl/Kd7Jk8', extension='.tar.gz',
            preferred=True)

    version('laghos-v1.0', git='https://github.com/mfem/mfem',
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

    variant('mpi', default=True,
        description='Enable MPI parallelism')
    variant('hypre', default=True,
        description='Required for MPI parallelism')
    variant('openmp', default=False,
        description='Enable OpenMP parallelism')
    variant('threadsafe', default=False,
        description=('Enable thread safe features.'
            ' Required for OpenMP.'
            ' May cause minor performance issues.'))
    variant('superlu-dist', default=False,
        description='Enable MPI parallel, sparse direct solvers')
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
    variant('examples', default=False,
        description='Build and install examples')
    variant('miniapps', default=False,
        description='Build and install miniapps')

    conflicts('+mpi', when='~hypre')
    conflicts('+suite-sparse', when='~lapack')
    conflicts('+superlu-dist', when='@:3.1')
    conflicts('+netcdf', when='@:3.1')

    depends_on('hypre', when='+hypre')
    depends_on('blas', when='+lapack')
    depends_on('blas', when='+suite-sparse')
    depends_on('lapack', when='+lapack')
    depends_on('lapack', when='+suite-sparse')

    depends_on('mpi', when='+mpi')
    depends_on('metis')
    depends_on('parmetis', when='+superlu-dist')
    depends_on('metis@5:', when='+superlu-dist')
    depends_on('metis@5:', when='+suite-sparse ^suite-sparse@4.5:')

    depends_on('sundials@2.7:+hypre', when='+sundials')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('superlu-dist', when='@3.2: +superlu-dist')
    depends_on('petsc@3.8:', when='+petsc')

    depends_on('mpfr', when='+mpfr')
    depends_on('netcdf', when='@3.2: +netcdf')
    depends_on('zlib', when='@3.2: +netcdf')
    depends_on('hdf5', when='@3.2: +netcdf')
    depends_on('libunwind', when='+debug')
    depends_on('zlib', when='+gzstream')

    patch('mfem_ppc_build.patch', when='@3.2:3.3 arch=ppc64le')

    #
    # Note: Although MFEM does support CMake configuration, MFEM
    # development team indicates that vanilla GNU Make is the
    # preferred mode of configuration of MFEM and the mode most
    # likely to be up to date in supporting *all* of MFEM's
    # configuration options. So, don't use CMake
    #
    def install(self, spec, prefix):

        def yes_no(varstr):
            return 'YES' if varstr in self.spec else 'NO'

        metis5_str = 'NO'
        if '+superlu-dist' in spec or  \
            spec.satisfies('+suite-sparse ^suite-sparse@4.5:') or \
                spec['metis'].satisfies('@5:'):
                metis5_str = 'YES'

        threadsafe_str = 'NO'
        if '+openmp' in spec or '+threadsafe' in spec:
            threadsafe_str = 'YES'

        options = [
            'PREFIX=%s' % prefix,
            'MFEM_USE_MEMALLOC=YES',
            'MFEM_DEBUG=%s' % yes_no('+debug'),
            'CXX=%s' % env['CXX'],
            'MFEM_USE_LIBUNWIND=%s' % yes_no('+debug'),
            'MFEM_USE_GZSTREAM=%s' % yes_no('+gzstream'),
            'MFEM_USE_METIS_5=%s' % metis5_str,
            'MFEM_THREAD_SAFE=%s' % threadsafe_str,
            'MFEM_USE_MPI=%s' % yes_no('+mpi'),
            'MFEM_USE_LAPACK=%s' % yes_no('+lapack'),
            'MFEM_USE_SUPERLU=%s' % yes_no('+superlu-dist'),
            'MFEM_USE_SUITESPARSE=%s' % yes_no('+suite-sparse'),
            'MFEM_USE_SUNDIALS=%s' % yes_no('+sundials'),
            'MFEM_USE_PETSC=%s' % yes_no('+petsc'),
            'MFEM_USE_NETCDF=%s' % yes_no('+netcdf'),
            'MFEM_USE_MPFR=%s' % yes_no('+mpfr'),
            'MFEM_USE_OPENMP=%s' % yes_no('+openmp')]

        if '+mpi' in spec:
            options += ['MPICXX=%s' % spec['mpi'].mpicxx]

        if '+hypre' in spec:
            options += [
                'HYPRE_DIR=%s' % spec['hypre'].prefix,
                'HYPRE_OPT=-I%s' % spec['hypre'].prefix.include,
                'HYPRE_LIB=-L%s' % spec['hypre'].prefix.lib + ' -lHYPRE']

        if '+lapack' in spec:
            lapack_lib = (spec['lapack'].libs + spec['blas'].libs).ld_flags  # NOQA: ignore=E501
            options += [
                'LAPACK_OPT=-I%s' % spec['lapack'].prefix.include,
                'LAPACK_LIB=%s' % lapack_lib]

        if '+superlu-dist' in spec:
            metis_lib = '-L%s -lparmetis -lmetis' % spec['parmetis'].prefix.lib
            options += [
                'METIS_DIR=%s' % spec['parmetis'].prefix,
                'METIS_OPT=-I%s' % spec['parmetis'].prefix.include,
                'METIS_LIB=%s' % metis_lib]
            superlu_lib = '-L%s' % spec['superlu-dist'].prefix.lib
            superlu_lib += ' -lsuperlu_dist'
            options += [
                'SUPERLU_DIR=%s' % spec['superlu-dist'].prefix,
                'SUPERLU_OPT=-I%s' % spec['superlu-dist'].prefix.include,
                'SUPERLU_LIB=%s' % superlu_lib]
        else:
            metis_lib = '-L%s -lmetis' % spec['metis'].prefix.lib
            options += [
                'METIS_DIR=%s' % spec['metis'].prefix,
                'METIS_OPT=-I%s' % spec['metis'].prefix.include,
                'METIS_LIB=%s' % metis_lib]

        if '+suite-sparse' in spec:
            ssp = spec['suite-sparse'].prefix
            ss_lib = '-L%s' % ssp.lib
            if '@3.2:' in spec:
                ss_lib += ' -lklu -lbtf'
            ss_lib += (' -lumfpack -lcholmod -lcolamd' +
                       ' -lamd -lcamd -lccolamd -lsuitesparseconfig')
            no_rt = spec.satisfies('platform=darwin')
            if not no_rt:
                ss_lib += ' -lrt'
            ss_lib += (' ' + metis_lib + ' ' + lapack_lib)
            options += [
                'SUITESPARSE_DIR=%s' % ssp,
                'SUITESPARSE_OPT=-I%s' % ssp.include,
                'SUITESPARSE_LIB=%s' % ss_lib]

        if '+sundials' in spec:
            sundials_libs = (
                '-lsundials_arkode -lsundials_cvode'
                ' -lsundials_nvecserial -lsundials_kinsol')
            if '+mpi' in spec:
                sundials_libs += (
                    ' -lsundials_nvecparhyp -lsundials_nvecparallel')
            options += [
                'SUNDIALS_DIR=%s' % spec['sundials'].prefix,
                'SUNDIALS_OPT=-I%s' % spec['sundials'].prefix.include,
                'SUNDIALS_LIB=-L%s %s' % (spec['sundials'].prefix.lib,
                                          sundials_libs)]

        if '+petsc' in spec:
            f = open('%s/lib/pkgconfig/PETSc.pc' % spec['petsc'].prefix, 'r')
            for line in f:
                if re.search('^\s*Cflags: ', line):
                    petsc_opts = re.sub('^\s*Cflags: (.*)', '\\1', line)
                elif re.search('^\s*Libs.*: ', line):
                    petsc_libs = re.sub('^\s*Libs.*: (.*)', '\\1', line)
            f.close()
            options += [
                'PETSC_DIR=%s' % spec['petsc'].prefix,
                'PETSC_OPT=%s' % petsc_opts,
                'PETSC_LIB=-L%s -lpetsc %s' %
                (spec['petsc'].prefix.lib, petsc_libs)]

        if '+netcdf' in spec:
            np = spec['netcdf'].prefix
            zp = spec['zlib'].prefix
            h5p = spec['hdf5'].prefix
            nlib = '-L%s -lnetcdf ' % np.lib
            nlib += '-L%s -lhdf5_hl -lhdf5 ' % h5p.lib
            nlib += '-L%s -lz' % zp.lib
            options += [
                'NETCDF_DIR=%s' % np,
                'HDF5_DIR=%s' % h5p,
                'ZLIB_DIR=%s' % zp,
                'NETCDF_OPT=-I%s' % np.include,
                'NETCDF_LIB=%s' % nlib]

        if '+mpfr' in spec:
            options += ['MPFR_LIB=-L%s -lmpfr' % spec['mpfr'].prefix.lib]

        if '+openmp' in spec:
            options += ['OPENMP_OPT = %s' % self.compiler.openmp_flag]

        make('config', *options)
        make('lib')

        if self.run_tests:
            make('check')

        make('install')

        if '+examples' in spec:
            make('examples')
            install_tree('examples', join_path(prefix, 'examples'))

        if '+miniapps' in spec:
            make('miniapps')
            install_tree('miniapps', join_path(prefix, 'miniapps'))
