# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonEngineio(PythonPackage):
    """Engine.IO is the implementation of transport-based
    cross-browser/cross-device bi-directional communication
    layer for Socket.IO."""

    homepage = "http://python-engineio.readthedocs.io/en/latest/"
    url      = "https://github.com/miguelgrinberg/python-engineio/archive/v2.0.2.tar.gz"

    version('2.0.2', 'b91c6fa900905f9a96b86c3e141e2754')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:', type=('build', 'run'))
