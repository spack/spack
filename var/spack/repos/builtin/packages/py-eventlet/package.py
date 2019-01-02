# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEventlet(PythonPackage):
    """Concurrent networking library for Python"""

    homepage = "https://github.com/eventlet/eventlet"
    url      = "https://github.com/eventlet/eventlet/releases/download/v0.22.0/eventlet-0.22.0.tar.gz"

    version('0.22.0', 'a1199cecd44d7ce2ea624ac6c21db877')

    depends_on('py-setuptools', type='build')
    depends_on('py-greenlet@0.3:')
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3.99')
