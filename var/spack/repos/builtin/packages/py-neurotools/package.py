# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeurotools(PythonPackage):
    """A collection of tools for representing and anlyzing neuroscientific
    data."""

    homepage = "http://neuralensemble.org/NeuroTools"
    url      = "https://pypi.io/packages/source/n/neurotools/NeuroTools-0.3.1.tar.gz"

    version('0.3.1', sha256='a459420fc0e9ff6b59af28716ddb0c75d11a63b8db80a5f4844e0d7a90c2c653')

    depends_on('py-scipy', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-urllib3', type='run')
    depends_on('py-mpi4py', type='run')
    depends_on('py-tables', type='run')
    depends_on('py-pyaml', type='run')
    # py-interval is py2 only and most probably not used
    # depends_on('py-interval', type='run')

    patch('neurotools-0.3.1.patch', when='@0.3.1')
