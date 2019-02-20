# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages"""

    homepage = "https://importlib-metadata.readthedocs.io/en/latest/"
    url      = "https://files.pythonhosted.org/packages/af/6a/ef5cac9b429b974df7189bc35c974251b91c38bc9c7b74a0ed56cf0baf9a/importlib_metadata-0.8.tar.gz"

    version('0.8', sha256='b50191ead8c70adfa12495fba19ce6d75f2e0275c14c5a7beb653d6799b512bd')

    depends_on('py-setuptools', type='build')
    depends_on('py-configparser', type=('build', 'run'), when="^python@:3")
    depends_on('py-contextlib2', type=('build', 'run'), when="^python@:3")
    depends_on('py-pathlib2', type=('build', 'run'), when="^python@:3")
    depends_on('py-typing', type=('build', 'run'), when="^python@:3.5")
    depends_on('py-zipp@0.3.2:', type=('build', 'run'))
