# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDaskMpi(PythonPackage):
    """Deploying Dask using MPI4Py."""

    homepage = "https://github.com/dask/dask-mpi"
    url      = "https://pypi.io/packages/source/d/dask-mpi/dask-mpi-2.21.0.tar.gz"

    import_modules = ['dask_mpi']

    version('2.21.0', sha256='76e153fc8c58047d898970b33ede0ab1990bd4e69cc130c6627a96f11b12a1a7')
    version('2.0.0', sha256='774cd2d69e5f7154e1fa133c22498062edd31507ffa2ea19f4ab4d8975c27bc3')

    depends_on('py-dask@2.2:', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
