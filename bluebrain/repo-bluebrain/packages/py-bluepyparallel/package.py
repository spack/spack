# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepyparallel(PythonPackage):
    """Python library to run embarassingly parallel computations."""

    homepage = "https://bbpgitlab.epfl.ch/neuromath/bluepyparallel"
    git      = "git@bbpgitlab.epfl.ch:neuromath/bluepyparallel.git"

    version('0.0.5', tag='BluePyParallel-v0.0.5')

    depends_on('py-setuptools', type='build')

    depends_on('py-pandas@0.24:', type='run')
    depends_on('py-dask+dataframe+distributed@2.30:', type='run')
    depends_on('py-dask-mpi@2.21.0:', type='run')
    depends_on('py-mpi4py@3.0.3:', type='run')
    depends_on('py-tqdm@4.28.1:', type='run')
    depends_on('py-sqlalchemy@:1.3', type='run')
    depends_on('py-sqlalchemy-utils@0.36:', type='run')
    depends_on('py-ipyparallel@6.3:', type='run')
