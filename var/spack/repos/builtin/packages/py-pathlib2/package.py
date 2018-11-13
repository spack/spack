# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPathlib2(PythonPackage):
    """Backport of pathlib from python 3.4"""

    homepage = "https://pypi.python.org/pypi/pathlib2"
    url      = "https://pypi.io/packages/source/p/pathlib2/pathlib2-2.3.2.tar.gz"

    import_modules = ['pathlib2']

    version('2.3.2', 'fd76fb5d0baa798bfe12fb7965da97f8')
    version('2.1.0', '38e4f58b4d69dfcb9edb49a54a8b28d2')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-scandir', when='^python@:3.4', type=('build', 'run'))
