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

import os

class Espresso(Package):
    """
    QE is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials
    modeling at the nanoscale. It is based on density-functional theory, plane waves, and pseudopotentials.
    """
    homepage = 'http://quantum-espresso.org'
    url = 'http://www.qe-forge.org/gf/download/frsrelease/204/912/espresso-5.3.0.tar.gz'

    version('5.3.0', '6848fcfaeb118587d6be36bd10b7f2c3')

    variant('mpi', default=True, description='Build Quantum-ESPRESSO with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
    variant('scalapack', default=True, description='Enables scalapack support')
    variant('elpa', default=True, description='Use elpa as an eigenvalue solver')

    depends_on('blas')
    depends_on('lapack')

    depends_on('mpi', when='+mpi')
    depends_on('fftw~mpi', when='~mpi')
    depends_on('fftw+mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack+mpi')  # TODO : + mpi needed to avoid false dependencies installation

    def check_variants(self, spec):
        error = 'you cannot ask for \'+{variant}\' when \'+mpi\' is not active'
        if '+scalapack' in spec and '~mpi' in spec:
            raise RuntimeError(error.format(variant='scalapack'))
        if '+elpa' in spec and ('~mpi' in spec or '~scalapack' in spec):
            raise RuntimeError(error.format(variant='elpa'))

    def install(self, spec, prefix):
        from glob import glob
        self.check_variants(spec)

        options = ['-prefix=%s' % prefix.bin]

        if '+mpi' in spec:
            options.append('--enable-parallel')

        if '+openmp' in spec:
            options.append('--enable-openmp')

        if '+scalapack' in spec:
            options.append('--with-scalapack=yes')

        if '+elpa' in spec:
            options.append('--with-elpa=yes')

        # Add a list of directories to search
        search_list = []
        for name, dependency_spec in spec.dependencies.iteritems():
            search_list.extend([dependency_spec.prefix.lib,
                                dependency_spec.prefix.lib64])

        search_list = " ".join(search_list)
        options.append('LIBDIRS=%s' % search_list)
        options.append('F90=%s' % os.environ['FC'])

        configure(*options)
        make('all')

        if spec.architecture.startswith('darwin'):
            mkdirp(prefix.bin)
            for filename in glob("bin/*.x"):
                install(filename, prefix.bin)
        else:
            make('install')

