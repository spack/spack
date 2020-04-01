# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyParamiko(PythonPackage):
    """SSH2 protocol library"""

    homepage = "http://www.paramiko.org/"
    url      = "https://pypi.io/packages/source/p/paramiko/paramiko-2.1.2.tar.gz"

    version('2.1.2', sha256='5fae49bed35e2e3d45c4f7b0db2d38b9ca626312d91119b3991d0ecf8125e310')

    depends_on('py-setuptools',    type='build')
    depends_on('py-pyasn1@0.1.7:',        type=('build', 'run'))
    depends_on('py-cryptography@1.1:',    type=('build', 'run'))
