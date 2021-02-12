# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCurrent(PythonPackage):
    """Current module relative paths and imports"""

    homepage = "http://github.com/xflr6/current"
    pypi = "current/current-0.3.1.zip"

    version('0.3.6', sha256='5c86c705f2bcf21a08b3b133b462a3b1c4dc660fe977ea81bc6bcda24d8772c2')
    version('0.3.5', sha256='f368b2ed59271132f69ed5ca8490118ce891b722e85bec56e2aacf832d257fcd')
    version('0.3.4', sha256='64efe3a433f77e435ca409c7dfc120a70fbcaf6c627ef6a2bebf78bf3caeae8c')
    version('0.3.3', sha256='538c5d099e46199175ec40984c13708fe28ddf1da5c7daca643c9964f79a951b')
    version('0.3.2', sha256='254e5e95a9cf2029b3543bc076b61dc80a5eb6fcc06874a8651d64de4fce061f')
    version('0.3.1', sha256='207613dc19a6cc8e1a756f26e416733c8f82a70e4ae81103d22f483aae6492a8')

    depends_on('py-setuptools', type='build')
