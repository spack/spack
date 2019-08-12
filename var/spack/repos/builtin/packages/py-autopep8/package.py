# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAutopep8(PythonPackage):
    """autopep8 automatically formats Python code to conform to the
    PEP 8 style guide."""

    homepage = "https://github.com/hhatto/autopep8"
    url      = "https://pypi.io/packages/source/a/autopep8/autopep8-1.2.4.tar.gz"

    version('1.3.3', '8951f43748406015b663a54ab05d891a')
    version('1.2.4', 'fcea19c0c5e505b425e2a78afb771f5c')
    version('1.2.2', '3d97f9c89d14a0975bffd32a2c61c36c')

    extends('python', ignore='bin/pep8')
    depends_on('python@2.6:2.8,3.2:')

    depends_on('py-pycodestyle@1.5.7:1.7.0', type=('build', 'run'), when='@:1.2.4')
    depends_on('py-pycodestyle@2.3.0:', type=('build', 'run'), when='@1.3:')

    depends_on('py-setuptools', type='build')
