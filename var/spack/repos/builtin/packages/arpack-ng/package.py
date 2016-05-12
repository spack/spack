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
    """
    ARPACK-NG is a collection of Fortran77 subroutines designed to solve large scale eigenvalue problems.

    Important Features:

    * Reverse Communication Interface.
    * Single and Double Precision Real Arithmetic Versions for Symmetric,
      Non-symmetric, Standard or Generalized Problems.
    * Single and Double Precision Complex Arithmetic Versions for Standard or
      Generalized Problems.
    * Routines for Banded Matrices - Standard or Generalized Problems.
    * Routines for The Singular Value Decomposition.
    * Example driver routines that may be used as templates to implement numerous
      Shift-Invert strategies for all problem types, data types and precision.

    This project is a joint project between Debian, Octave and Scilab in order to
    provide a common and maintained version of arpack.

    Indeed, no single release has been published by Rice university for the last
    few years and since many software (Octave, Scilab, R, Matlab...) forked it and
    implemented their own modifications, arpack-ng aims to tackle this by providing
    a common repository and maintained versions.

    arpack-ng is replacing arpack almost everywhere.
    """
    homepage = 'https://github.com/opencollab/arpack-ng'
    url = 'https://github.com/opencollab/arpack-ng/archive/3.3.0.tar.gz'

    version('3.3.0', 'ed3648a23f0a868a43ef44c97a21bad5')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('mpi', default=False, description='Activates MPI support')

    # The function pdlamch10 does not set the return variable. This is fixed upstream
    # see https://github.com/opencollab/arpack-ng/issues/34
    patch('pdlamch10.patch', when='@3.3:')

    depends_on('blas')
    depends_on('lapack')
    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool@2.4.2:')

    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
        # Apparently autotools are not bootstrapped
        # TODO: switch to use the CMake build in the next version
        # rather than bootstrapping.
        which('libtoolize')()
        bootstrap = Executable('./bootstrap')

        options = ['--prefix=%s' % prefix]

        if '+mpi' in spec:
            options.extend([
                '--enable-mpi',
                'F77=mpif77' #FIXME: avoid hardcoding MPI wrapper names
            ])

        if '~shared' in spec:
            options.append('--enable-shared=no')

        bootstrap()
        configure(*options)
        make()
        make('install')
