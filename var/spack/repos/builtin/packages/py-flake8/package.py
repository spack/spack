# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    url      = "https://github.com/PyCQA/flake8/archive/3.7.8.tar.gz"

    version('3.7.8',  sha256='201720797dc9691dd349819994e4a0bc281b70ee2ff77b0c928bb1d3c5aa9810')
    version('3.7.7',  sha256='b3f76b02351008dc772276e74b09dd3d4b5c567ff8c6ab573352cb8fd7007444')
    version('3.5.0', '4e312803bbd8e4a1e566ffac887ae647')
    version('3.0.4', 'cf2a7d8c92070f7b62253404ffb54df7')
    version('2.5.4', '366dd1de6c300254c830b81e66979f06')

    extends('python', ignore='bin/(pyflakes|pycodestyle)')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on('py-setuptools@30:', type=('build', 'run'))

    # Flake8 uses ranges for its dependencies to enforce a stable list of
    # error codes within each minor release:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    # http://flake8.pycqa.org/en/latest/internal/releases.html#releasing-flake8

    # Flake8 3.7.X
    # FIXME @0.3.0:0.3.999 causes concretization to hang
    depends_on('py-entrypoints@0.3',           when='@3.7.0:3.7.999', type=('build', 'run'))
    depends_on('py-pyflakes@2.1.0:2.1.999',    when='@3.7.0:3.7.999', type=('build', 'run'))
    depends_on('py-pycodestyle@2.5.0:2.5.999', when='@3.7.0:3.7.999', type=('build', 'run'))
    depends_on('py-mccabe@0.6.0:0.6.999',      when='@3.7.0:3.7.999', type=('build', 'run'))

    # Flake8 3.5.X
    depends_on('py-pyflakes@1.5:1.6',     when='@3.5.0:3.5.999', type=('build', 'run'))
    depends_on('py-pycodestyle@2.0:2.4',  when='@3.5.0:3.5.999', type=('build', 'run'))
    depends_on('py-mccabe@0.6.0:0.6.999', when='@3.5.0:3.5.999', type=('build', 'run'))

    # Flake8 3.0.X
    depends_on('py-pyflakes@0.8.1:1.1,1.2.3:1.2.999', when='@3.0.0:3.0.999', type=('build', 'run'))
    depends_on('py-pycodestyle@2.0.0:2.0.999',        when='@3.0.0:3.0.999', type=('build', 'run'))
    depends_on('py-mccabe@0.5.0:0.5.999',             when='@3.0.0:3.0.999', type=('build', 'run'))

    # Flake8 2.5.X
    depends_on('py-pyflakes@0.8.1:1.0',               when='@2.5.0:2.5.999', type=('build', 'run'))
    depends_on('py-pycodestyle@1.5.7:1.5.999,1.6.3:', when='@2.5.0:2.5.999', type=('build', 'run'))
    depends_on('py-mccabe@0.2.1:0.4',                 when='@2.5.0:2.5.999', type=('build', 'run'))

    # Python version-specific backports
    depends_on('py-enum34',       when='@3.0.0: ^python@:3.3', type=('build', 'run'))
    depends_on('py-typing',       when='@3.7.0: ^python@:3.4', type=('build', 'run'))
    depends_on('py-configparser', when='@3.0.0: ^python@:3.1', type=('build', 'run'))
    depends_on('py-functools32',  when='@3.7.4: ^python@:3.1', type=('build', 'run'))

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)
