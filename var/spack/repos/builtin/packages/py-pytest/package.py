# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytest(PythonPackage):
    """pytest: simple powerful testing with Python."""

    homepage = "http://pytest.org/"
    url      = "https://pypi.io/packages/source/p/pytest/pytest-5.1.1.tar.gz"

    import_modules = ['pytest']

    version('5.1.1', sha256='c3d5020755f70c82eceda3feaf556af9a341334414a8eca521a18f463bcead88')
    version('4.6.5', sha256='8fc39199bdda3d9d025d3b1f4eb99a192c20828030ea7c9a0d2840721de7d347')
    version('4.3.0', 'e1913b607c5c4e7d886ba6f13a43617e')
    version('3.7.2', 'd12d0d556a21fd8633e105f1a8d5a0f9')
    version('3.7.1', '2704e16bb2c11af494167f80a7cd37c4')
    version('3.5.1', 'ffd870ee3ca561695d2f916f0f0f3c0b')
    version('3.0.7', '89c60546507dc7eb6e9e40a6e9f720bd')
    version('3.0.2', '61dc36e65a6f6c11c53b1388e043a9f5')

    depends_on('python@3.5:', when='@5:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@3.3:4', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', when='@:3.2', type=('build', 'run'))

    # Most Python packages only require setuptools as a build dependency.
    # However, pytest requires setuptools during runtime as well.
    # FIXME: May no longer be needed at runtime, see:
    # https://github.com/pytest-dev/pytest/pull/5063
    depends_on('py-setuptools@40.0:', when='@3.9.2:', type=('build', 'run'))
    depends_on('py-setuptools@30.3:', when='@3.9.0:3.9.1', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', when='@3.1:', type='build')
    depends_on('py-py@1.5.0:', type=('build', 'run'))
    depends_on('py-py@1.4.33:', when='@3.1.2:3.2.3,3.2.5:3.2.999', type=('build', 'run'))
    depends_on('py-py@1.4.33:1.4.999', when='@3.2.4', type=('build', 'run'))
    depends_on('py-py@1.4.29:', when='@:3.1.1', type=('build', 'run'))
    depends_on('py-six@1.10.0:', when='@3.3:4', type=('build', 'run'))
    depends_on('py-packaging', when='@4.6:', type=('build', 'run'))
    depends_on('py-attrs@17.2.0:', when='@3.3:3.4', type=('build', 'run'))
    depends_on('py-attrs@17.4.0:', when='@3.5:', type=('build', 'run'))
    depends_on('py-more-itertools@4.0.0:', when='@3.5.1:', type=('build', 'run'))
    depends_on('py-more-itertools@4.0.0:6.0.0', when='@4.2.1:4.6.5 ^python@:2', type=('build', 'run'))
    depends_on('py-atomicwrites@1.0:', when='@3.6:', type=('build', 'run'))
    depends_on('py-pluggy@0.12:0.999', when='@4.6:', type=('build', 'run'))
    depends_on('py-pluggy@0.9.0:0.9.999,0.11:0.999', when='@4.5.0:4.5.999', type=('build', 'run'))
    depends_on('py-pluggy@0.11:', when='@4.4.2:4.4.999', type=('build', 'run'))
    depends_on('py-pluggy@0.9:', when='@4.4.0:4.4.1', type=('build', 'run'))
    depends_on('py-pluggy@0.7:', when='@3.7:4.3', type=('build', 'run'))
    depends_on('py-pluggy@0.5:0.7', when='@3.6.4:3.6.999', type=('build', 'run'))
    depends_on('py-pluggy@0.5:0.6', when='@:3.6.3', type=('build', 'run'))
    depends_on('py-funcsigs@1.0:', when='@4.4: ^python@:2', type=('build', 'run'))
    depends_on('py-funcsigs', when='@3.3:4.3 ^python@:2', type=('build', 'run'))
    depends_on('py-pathlib2@2.2.0:', when='@3.7.1: ^python@:3.5', type=('build', 'run'))
    depends_on('py-pathlib2', when='@3.7.0 ^python@:3.5', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.12:', when='@4.6:5.0', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.12:', when='@5.1: ^python@:3.7', type=('build', 'run'))
    depends_on('py-wcwidth', when='@4.5:', type=('build', 'run'))
