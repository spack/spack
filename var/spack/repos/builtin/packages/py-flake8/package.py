# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    url      = "https://github.com/PyCQA/flake8/archive/3.0.4.tar.gz"

    version('3.7.7',  sha256='b3f76b02351008dc772276e74b09dd3d4b5c567ff8c6ab573352cb8fd7007444')
    version('3.5.0', '4e312803bbd8e4a1e566ffac887ae647')
    version('3.0.4', 'cf2a7d8c92070f7b62253404ffb54df7')
    version('2.5.4', '366dd1de6c300254c830b81e66979f06')

    extends('python', ignore='bin/(pyflakes|pycodestyle)')
    depends_on('python@2.7:2.8,3.4:')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on('py-setuptools@30:', type=('build', 'run'))

    # entrypoints >= 0.3.0, < 0.4.0
    # FIXME @0.3.0:0.3.999 causes concretization to hang
    depends_on('py-entrypoints@0.3', when='@3.7.7', type=('build', 'run'))

    # pyflakes >= 2.1.0, < 2.2.0
    depends_on('py-pyflakes@2.1.0:2.1.999', when='@3.7.7', type=('build', 'run'))
    # pyflakes >= 1.5.0, < 1.7.0
    depends_on('py-pyflakes@1.5.0:1.6.999', when='@3.5.0', type=('build', 'run'))
    # pyflakes >= 0.8.1, != 1.2.0, != 1.2.1, != 1.2.2, < 1.3.0
    depends_on('py-pyflakes@0.8.1:1.1.0,1.2.3:1.2.3', when='@3.0.4', type=('build', 'run'))
    # pyflakes >= 0.8.1, < 1.1
    depends_on('py-pyflakes@0.8.1:1.0.0', when='@2.5.4', type=('build', 'run'))

    # pycodestyle >= 2.5.0, < 2.6.0
    depends_on('py-pycodestyle@2.5.0:2.5.999', when='@3.7.7', type=('build', 'run'))
    # pycodestyle >= 2.3.0, < 2.4.0
    depends_on('py-pycodestyle@2.3.0:2.3.999', when='@3.5.0', type=('build', 'run'))
    # pycodestyle >= 2.0.0, < 2.1.0
    depends_on('py-pycodestyle@2.0.0:2.0.999', when='@3.0.4', type=('build', 'run'))
    # pep8 >= 1.5.7, != 1.6.0, != 1.6.1, != 1.6.2
    depends_on('py-pycodestyle@1.5.7,1.7.0:', when='@2.5.4', type=('build', 'run'))

    # mccabe >= 0.6.0, < 0.7.0
    depends_on('py-mccabe@0.6.0:0.6.999', when='@3.5.0,3.7.7', type=('build', 'run'))
    # mccabe >= 0.5.0, < 0.6.0
    depends_on('py-mccabe@0.5.0:0.5.999', when='@3.0.4', type=('build', 'run'))
    # mccabe >= 0.2.1, < 0.5
    depends_on('py-mccabe@0.2.1:0.4.0', when='@2.5.4', type=('build', 'run'))

    depends_on('py-configparser', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.1', type=('build', 'run'))

    # py-enum34 provides enum module from Python 3.4 for Python
    # versions 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, and 3.3; use built-in enum
    # module for Python versions 3.4 and later
    depends_on('py-enum34', when='^python@2.4:2.7.999,3.1:3.3.999',
               type=('build', 'run'))

    depends_on('py-functools32', when='@3.7.7: ^python@:3.1.999', type=('build', 'run'))
    depends_on('py-typing', when='@3.7.7: ^python@:3.4.999', type=('build', 'run'))

    depends_on('py-nose', type='test')

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)
