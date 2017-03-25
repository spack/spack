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


class PyH5py(PythonPackage):
    """The h5py package provides both a high- and low-level interface to the
    HDF5 library from Python."""

    homepage = "https://pypi.python.org/pypi/h5py"
    url      = "https://pypi.python.org/packages/source/h/h5py/h5py-2.4.0.tar.gz"

    version('2.6.0', 'ec476211bd1de3f5ac150544189b0bf4')
    version('2.5.0', '6e4301b5ad5da0d51b0a1e5ac19e3b74')
    version('2.4.0', '80c9a94ae31f84885cc2ebe1323d6758')

    variant('mpi', default=True, description='Build with MPI support')

    # Build dependencies
    depends_on('py-cython@0.19:', type='build')
    depends_on('pkg-config', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('hdf5@1.8.4:')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))

    # Build and runtime dependencies
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))

    # Runtime dependencies
    depends_on('py-six', type=('build', 'run'))

    phases = ['configure', 'install']

    def configure(self, spec, prefix):
        self.setup_py('configure', '--hdf5={0}'.format(spec['hdf5'].prefix))

        if '+mpi' in spec:
            env['CC'] = spec['mpi'].mpicc
            self.setup_py('configure', '--mpi')
