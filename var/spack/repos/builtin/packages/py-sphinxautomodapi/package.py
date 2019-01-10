# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxautomodapi(PythonPackage):
    """Provides Sphinx directives to autogenerate API documentation pages"""

    homepage = "https://sphinx-automodapi.readthedocs.io/en/latest/"
    url      = "https://github.com/astropy/sphinx-automodapi/archive/v0.9.tar.gz"

    version('0.9', '017817812e9266319fdcfcc89ddfbe570935ca87a3bda62d61c8507cf1337aa8')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx@1.3:', type=('build', 'run'))
