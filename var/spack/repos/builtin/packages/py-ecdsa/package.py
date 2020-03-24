# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEcdsa(PythonPackage):
    """ECDSA cryptographic signature library (pure python)"""

    homepage = "https://github.com/warner/python-ecdsa"
    url      = "https://files.pythonhosted.org/packages/source/e/ecdsa/ecdsa-0.13.2.tar.gz"

    version('0.13.2', sha256='5c034ffa23413ac923541ceb3ac14ec15a0d2530690413bff58c12b80e56d884')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('openssl',       type='test')
