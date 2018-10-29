# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonSocketio(PythonPackage):
    """Python implementation of the Socket.IO realtime server."""

    homepage = "https://github.com/miguelgrinberg/python-socketio"
    url      = "https://pypi.io/packages/source/p/python-socketio/python-socketio-1.8.4.tar.gz"

    version('1.8.4', '9de73990f6c32c701278c01b0fa1a0c3')

    variant('eventlet', default=True,
            description="Pulls in optional eventlet dependency, required"
                        " for using the zmq implementation.")

    depends_on('py-setuptools',                 type='build')
    depends_on('py-six@1.9.0:',                 type=("build", "run"))
    depends_on('py-python-engineio@1.2.1:',     type=("build", "run"))
    depends_on('py-eventlet', when='+eventlet', type=("build", "run"))
