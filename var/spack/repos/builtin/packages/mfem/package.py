##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from spack import *
import glob
import string


class Mfem(Package):
    """Free, lightweight, scalable C++ library for finite element methods."""

    homepage = 'http://www.mfem.org'
    url      = 'https://github.com/mfem/mfem'

    version('3.2',
            '2938c3deed4ec4f7fd5b5f5cfe656845282e86e2dcd477d292390058b7b94340',
            url='http://goo.gl/Y9T75B', expand=False, preferred=True)

    version('3.1',
            '841ea5cf58de6fae4de0f553b0e01ebaab9cd9c67fa821e8a715666ecf18fc57',
            url='http://goo.gl/xrScXn', expand=False)
#    version('3.1', git='https://github.com/mfem/mfem.git',
#            commit='dbae60fe32e071989b52efaaf59d7d0eb2a3b574')

    variant('metis', default=False, description='Activate support for metis')
    variant('hypre', default=False, description='Activate support for hypre')
    variant('suite-sparse', default=False,
            description='Activate support for SuiteSparse')
    variant('mpi', default=False, description='Activate support for MPI')
    variant('lapack', default=False, description='Activate support for LAPACK')
    variant('debug', default=False, description='Build debug version')

    depends_on('blas', when='+lapack')
    depends_on('lapack', when='+lapack')

    depends_on('mpi', when='+mpi')
    depends_on('metis', when='+mpi')
    depends_on('hypre', when='+mpi')

    depends_on('hypre', when='+hypre')

    depends_on('metis@4:', when='+metis')

    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('blas', when='+suite-sparse')
    depends_on('lapack', when='+suite-sparse')
    depends_on('metis@5:', when='+suite-sparse ^suite-sparse@4.5:')
    depends_on('cmake', when='^metis@5:', type='build')

    def check_variants(self, spec):
        if '+mpi' in spec and ('+hypre' not in spec or '+metis' not in spec):
            raise InstallError('mfem+mpi must be built with +hypre ' +
                               'and +metis!')
        if '+suite-sparse' in spec and ('+metis' not in spec or
                                        '+lapack' not in spec):
            raise InstallError('mfem+suite-sparse must be built with ' +
                               '+metis and +lapack!')
        if 'metis@5:' in spec and '%clang' in spec and (
                '^cmake %gcc' not in spec):
            raise InstallError('To work around CMake bug with clang, must ' +
                               'build mfem with mfem[+variants] %clang ' +
                               '^cmake %gcc to force CMake to build with gcc')
        return

    def install(self, spec, prefix):
        self.check_variants(spec)

        options = ['PREFIX=%s' % prefix]

        if '+lapack' in spec:
            lapack_lib = (spec['lapack'].lapack_libs + spec['blas'].blas_libs).ld_flags  # NOQA: ignore=E501
            options.extend([
                'MFEM_USE_LAPACK=YES',
                'LAPACK_OPT=-I%s' % spec['lapack'].prefix.include,
                'LAPACK_LIB=%s' % lapack_lib])

        if '+hypre' in spec:
            options.extend([
                'HYPRE_DIR=%s' % spec['hypre'].prefix,
                'HYPRE_OPT=-I%s' % spec['hypre'].prefix.include,
                'HYPRE_LIB=-L%s' % spec['hypre'].prefix.lib +
                ' -lHYPRE'])

        if '+metis' in spec:
            metis_lib = '-L%s -lmetis' % spec['metis'].prefix.lib
            if spec['metis'].satisfies('@5:'):
                metis_str = 'MFEM_USE_METIS_5=YES'
            else:
                metis_str = 'MFEM_USE_METIS_5=NO'
            options.extend([
                metis_str,
                'METIS_DIR=%s' % spec['metis'].prefix,
                'METIS_OPT=-I%s' % spec['metis'].prefix.include,
                'METIS_LIB=%s' % metis_lib])

        if '+mpi' in spec:
            options.extend(['MFEM_USE_MPI=YES'])

        if '+suite-sparse' in spec:
            ssp = spec['suite-sparse'].prefix
            ss_lib = '-L%s' % ssp.lib
            ss_lib += (' -lumfpack -lcholmod -lcolamd -lamd -lcamd' +
                       ' -lccolamd -lsuitesparseconfig')

            no_librt_archs = ['darwin-i686', 'darwin-x86_64']
            no_rt = any(map(lambda a: spec.satisfies('=' + a),
                            no_librt_archs))
            if not no_rt:
                ss_lib += ' -lrt'
            ss_lib += (' ' + metis_lib + ' ' + lapack_lib)

            options.extend(['MFEM_USE_SUITESPARSE=YES',
                            'SUITESPARSE_DIR=%s' % ssp,
                            'SUITESPARSE_OPT=-I%s' % ssp.include,
                            'SUITESPARSE_LIB=%s' % ss_lib])

        if '+debug' in spec:
            options.extend(['MFEM_DEBUG=YES'])

        # Dirty hack to cope with URL redirect
        tgz_file = string.split(self.url, '/')[-1]
        tar = which('tar')
        tar('xzvf', tgz_file)
        cd(glob.glob('mfem*')[0])
        # End dirty hack to cope with URL redirect

        make('config', *options)
        make('all')

        # Run a small test before installation
        args = ['-m', join_path('data', 'star.mesh'), '--no-visualization']
        if '+mpi' in spec:
            Executable(join_path(spec['mpi'].prefix.bin,
                                 'mpirun'))('-np',
                                            '4',
                                            join_path('examples', 'ex1p'),
                                            *args)
        else:
            Executable(join_path('examples', 'ex1'))(*args)

        make('install')
