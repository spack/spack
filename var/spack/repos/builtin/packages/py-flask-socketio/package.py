##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class PyFlaskSocketio(PythonPackage):
    """Flask-SocketIO gives Flask applications access to low latency
    bi-directional communications between the clients and the server.
    The client-side application can use any of the SocketIO official clients
    libraries in Javascript, C++, Java and Swift, or any compatible client to
    establish a permanent connection to the server.
    """

    homepage = "https://flask-socketio.readthedocs.io"
    url      = "https://pypi.io/packages/source/F/Flask-SocketIO/Flask-SocketIO-2.9.6.tar.gz"

    version('2.9.6', 'bca83faf38355bd91911f2f140f9b50f')

    depends_on('py-setuptools',             type='build')
    depends_on('py-flask@0.9:',             type=('build', 'run'))
    depends_on('py-python-socketio@1.6.1:', type=('build', 'run'))
    depends_on('py-werkzeug',               type=('build', 'run'))
