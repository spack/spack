# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyCryptography(PythonPackage):
    """cryptography is a package which provides cryptographic recipes
       and primitives to Python developers"""

    homepage = "https://pypi.python.org/pypi/cryptography"
    url      = "https://pypi.io/packages/source/c/cryptography/cryptography-1.8.1.tar.gz"

    version('2.3.1', '8d10113ca826a4c29d5b85b2c4e045ffa8bad74fb525ee0eceb1d38d4c70dfd6')
    version('1.8.1', '9f28a9c141995cd2300d0976b4fac3fb')

    # dependencies taken from https://github.com/pyca/cryptography/blob/master/setup.py
    depends_on('py-setuptools@20.5:',   type='build')
    depends_on('py-cffi@1.4.1:',        type=('build', 'run'))
    depends_on('py-asn1crypto@0.21.0:', type=('build', 'run'))
    depends_on('py-six@1.4.1:',         type=('build', 'run'))
    depends_on('py-idna@2.1:',          type=('build', 'run'))
    depends_on('py-enum34',             type=('build', 'run'), when='^python@:3.4')
    depends_on('py-ipaddress',          type=('build', 'run'), when='^python@:3.3')
    depends_on('openssl@:1.0', when='@:1.8.1')
    depends_on('openssl')
