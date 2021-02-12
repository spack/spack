# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestMock(PythonPackage):
    """Thin-wrapper around the mock package for easier use with py.test"""

    homepage = "https://github.com/pytest-dev/pytest-mock"
    pypi = "pytest-mock/pytest-mock-1.11.1.tar.gz"

    version('3.5.1',  sha256='a1e2aba6af9560d313c642dae7e00a2a12b022b80301d9d7fc8ec6858e1dd9fc')
    version('3.5.0',  sha256='4992db789175540d40a193bc60e987b1e69f1a989adad525a44e581c82149b14')
    version('3.4.0',  sha256='c3981f5edee6c4d1942250a60d9b39d38d5585398de1bfce057f925bdda720f4')
    version('3.3.1',  sha256='a4d6d37329e4a893e77d9ffa89e838dd2b45d5dc099984cf03c703ac8411bb82')
    version('3.3.0',  sha256='1d146a6e798b9e6322825e207b4e0544635e679b69253e6e01a221f45945d2f6')
    version('3.2.0',  sha256='7122d55505d5ed5a6f3df940ad174b3f606ecae5e9bc379569cdcbd4cd9d2b83')
    version('3.1.1',  sha256='636e792f7dd9e2c80657e174c04bf7aa92672350090736d82e97e92ce8f68737')
    version('3.1.0',  sha256='ce610831cedeff5331f4e2fc453a5dd65384303f680ab34bee2c6533855b431c')
    version('3.0.0',  sha256='a4494016753a30231f8519bfd160242a0f3c8fb82ca36e7b6f82a7fb602ac6b8')
    version('2.0.0',  sha256='b35eb281e93aafed138db25c8772b95d3756108b601947f89af503f8c629413f')
    version('1.13.0', sha256='e24a911ec96773022ebcc7030059b57cd3480b56d4f5d19b7c370ec635e6aed5')
    version('1.12.1', sha256='96a0cebc66e09930be2a15b03333d90b59584d3fb011924f81c14b50ee0afbba')
    version('1.12.0', sha256='fff6cbd15a05f104062aa778e1ded35927d3d29bb1164218b140678fb368e32b')
    version('1.11.2', sha256='ea502c3891599c26243a3a847ccf0b1d20556678c528f86c98e3cd6d40c5cf11')
    version('1.11.1', sha256='f1ab8aefe795204efe7a015900296d1719e7bf0f4a0558d71e8599da1d1309d0')
    version('1.2',    sha256='f78971ed376fcb265255d1e4bb313731b3a1be92d7f3ecb19ea7fedc4a56fd0f',
            url='https://pypi.io/packages/source/p/pytest-mock/pytest-mock-1.2.zip')

    extends('python', ignore=r'bin/*')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-pytest@2.7:', type=('build', 'run'))
