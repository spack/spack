# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEtelemetry(PythonPackage):
    """A lightweight python client to communicate with the etelemetry server"""

    homepage = "https://github.com/sensein/etelemetry-client"
    url      = "https://github.com/sensein/etelemetry-client/archive/refs/tags/v0.2.2.tar.gz"

    version('0.2.2', sha256='bfec416552d248ad0f50b90ba5ff015e825ad70e4a87f7a06cc7da6d19152897')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-ci-info@0.2.0:', type=('build', 'run'))
