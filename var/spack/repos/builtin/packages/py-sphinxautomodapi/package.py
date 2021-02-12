# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxautomodapi(PythonPackage):
    """Provides Sphinx directives to autogenerate API documentation pages"""

    homepage = "https://sphinx-automodapi.readthedocs.io/en/latest/"
    pypi = "sphinx-automodapi/sphinx-automodapi-0.9.tar.gz"

    version('0.13', sha256='e1019336df7f7f0bcbf848eff7b84e7bef71691a57d8b5bda9107a2a046a226a')
    version('0.12', sha256='a1338bc0a7f5c9bb317ecf7c7abd489c7cff452098205ef5110f733570516ac0')
    version('0.11', sha256='4f61015db8c9a65809a41b1f609d827c99dc2c7b0179aedc4f64fc7d7aeec9e7')
    version('0.10', sha256='5c989bfe37f555f635e8fbb650859df391556981f5a436507fb3241794fd26c6')
    version('0.9', sha256='71a69e1a7ab8d849f416d7431db854d7b1925f749ba6345bc7d88f288892871d')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx@1.3:', type=('build', 'run'))
