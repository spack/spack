# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibResources(PythonPackage):
    """Provides for access to resources in Python packages"""

    homepage = "https://importlib-resources.readthedocs.io/en/latest/"
    url      = "https://files.pythonhosted.org/packages/83/a4/ce09af12e1a91b5b77cefc893ef5054619553734c5b42f143d93ed581744/importlib_resources-1.0.2.tar.gz"

    version('1.0.2', sha256='d3279fd0f6f847cced9f7acc19bd3e5df54d34f93a2e7bb5f238f81545787078')

    depends_on('py-setuptools', type='build')
    depends_on('py-pathlib2', type=('build', 'run'), when='^python@:3')
    depends_on('py-typing', type=('build', 'run'), when='^python@:3.5')
