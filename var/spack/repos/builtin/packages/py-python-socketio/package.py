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
