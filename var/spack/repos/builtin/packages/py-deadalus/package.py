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


class PyDeadalus(PythonPackage):
    """Dedalus is a flexible framework for solving partial differential equations
    using spectral methods."""

    homepage = "http://dedalus-project.readthedocs.io"
    url      = "https://bitbucket.org/dedalus-project/dedalus/get/default.tar.bz2"

    version('devel', hg='https://bitbucket.org/dedalus-project/dedalus')

    depends_on('py-cython@0.22:', type='build')
    depends_on('py-docopt')
    depends_on('py-h5py@2.6.0:')
    depends_on('mercurial', type='build')
    depends_on('py-hgapi', type='build')  # that is a guess...
    depends_on('py-matplotlib')
    depends_on('py-mpi4py@2.0.0:')
    depends_on('py-numpy')
    depends_on('py-pathlib')
    depends_on('py-scipy@0.13.0:')
    depends_on('fftw')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('FFTW_PATH', self.spec['fftw'].prefix)
        spack_env.set('MPI_PATH', self.spec['mpi'].prefix)

    def build(self, spec, prefix):
        args = self.build_args(spec, prefix)
        args.append('--inplace')

        self.setup_py('build_ext', *args)
