# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestXdist(PythonPackage):
    """py.test xdist plugin for distributed testing and loop-on-failing mode"""

    homepage = "https://github.com/pytest-dev/pytest-xdist"
    url      = "https://pypi.io/packages/source/p/pytest-xdist/pytest-xdist-1.16.0.tar.gz"

    version('1.16.0', '68dabf856981ad93b14960b098b05bff')

    depends_on('py-setuptools',    type='build')
    depends_on('py-execnet@1.1:',  type=('build', 'run'))
    depends_on('py-pytest@2.7.0:', type=('build', 'run'))
    depends_on('py-py@1.4.22:',    type=('build', 'run'))
