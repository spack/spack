# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurotools(PythonPackage):
    """NeuroTools is a collection of tools for representing and anlyzing neuroscientific data."""

    homepage = "http://neuralensemble.org/NeuroTools"
    url      = "https://pypi.io/packages/source/n/neurotools/NeuroTools-0.3.1.tar.gz"

    version('0.3.1', '67d1c4b6bee55ed9ab50d5daccc0f573')

    depends_on('py-scipy', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-urllib3', type='run')
    depends_on('py-mpi4py', type='run')
    depends_on('py-pytables', type='run')
    depends_on('py-pyaml', type='run')
    depends_on('py-rpy2', type='run')
