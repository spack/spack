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


class ArpackNg(Package):
    """ARPACK-NG is a collection of Fortran77 subroutines designed to solve large
    scale eigenvalue problems.

    Important Features:

    * Reverse Communication Interface.
    * Single and Double Precision Real Arithmetic Versions for Symmetric,
      Non-symmetric, Standard or Generalized Problems.
    * Single and Double Precision Complex Arithmetic Versions for Standard or
      Generalized Problems.
    * Routines for Banded Matrices - Standard or Generalized Problems.
    * Routines for The Singular Value Decomposition.
    * Example driver routines that may be used as templates to implement
      numerous Shift-Invert strategies for all problem types, data types and
      precision.

    This project is a joint project between Debian, Octave and Scilab in order
    to provide a common and maintained version of arpack.

    Indeed, no single release has been published by Rice university for the
    last few years and since many software (Octave, Scilab, R, Matlab...)
    forked it and implemented their own modifications, arpack-ng aims to tackle
    this by providing a common repository and maintained versions.

    arpack-ng is replacing arpack almost everywhere.
    """

    homepage = 'https://github.com/opencollab/arpack-ng'
    url = 'https://github.com/opencollab/arpack-ng/archive/3.3.0.tar.gz'

    version('3.4.0', 'ae9ca13f2143a7ea280cb0e2fd4bfae4')
    version('3.3.0', 'ed3648a23f0a868a43ef44c97a21bad5')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Activates MPI support')

    # The function pdlamch10 does not set the return variable.
    # This is fixed upstream
    # see https://github.com/opencollab/arpack-ng/issues/34
    patch('pdlamch10.patch', when='@3.3.0')

    patch('make_install.patch', when='@3.4.0')
    patch('parpack_cmake.patch', when='@3.4.0')

    depends_on('blas')
    depends_on('lapack')
    depends_on('automake', when='@3.3.0', type='build')
    depends_on('autoconf', when='@3.3.0', type='build')
    depends_on('libtool@2.4.2:', when='@3.3.0', type='build')
    depends_on('cmake@2.8.6:', when='@3.4.0:', type='build')

    depends_on('mpi', when='+mpi')

    @when('@3.4.0:')
    def install(self, spec, prefix):

        options = ['-DEXAMPLES=ON']
        options.extend(std_cmake_args)
        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        # Make sure we use Spack's blas/lapack:
        lapack_libs = spec['lapack'].libs.joined(';')
        blas_libs = spec['blas'].libs.joined(';')

        options.extend([
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS={0}'.format(spec['lapack'].prefix.include),
            '-DLAPACK_LIBRARIES={0}'.format(lapack_libs),
            '-DBLAS_FOUND=true',
            '-DBLAS_INCLUDE_DIRS={0}'.format(spec['blas'].prefix.include),
            '-DBLAS_LIBRARIES={0}'.format(blas_libs)
        ])

        if '+mpi' in spec:
            options.append('-DMPI=ON')

        # TODO: -DINTERFACE64=ON

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')

        cmake('.', *options)
        make()
        if self.run_tests:
            make('test')
        make('install')

    @when('@3.3.0')
    def install(self, spec, prefix):
        # Apparently autotools are not bootstrapped
        which('libtoolize')()
        bootstrap = Executable('./bootstrap')

        options = ['--prefix=%s' % prefix]

        if '+mpi' in spec:
            options.extend([
                '--enable-mpi',
                'F77=%s' % spec['mpi'].mpif77
            ])

        options.extend([
            '--with-blas={0}'.format(spec['blas'].libs.ld_flags),
            '--with-lapack={0}'.format(spec['lapack'].libs.ld_flags)
        ])
        if '+shared' not in spec:
            options.append('--enable-shared=no')

        bootstrap()
        configure(*options)
        make()
        if self.run_tests:
            make('check')
        make('install')
