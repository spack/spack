# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymysql(PythonPackage):
    """Pure-Python MySQL client library"""

    homepage = "https://github.com/PyMySQL/PyMySQL/"
    pypi = "pymysql/PyMySQL-0.9.2.tar.gz"

    version('1.0.2',  sha256='816927a350f38d56072aeca5dfb10221fe1dc653745853d30a216637f5d7ad36')
    version('1.0.1',  sha256='b46be62180008086fa9365a91c39a8853066ea5e8cde3a1e24491fb7de4b9286')
    version('1.0.0',  sha256='b2508a7dc6b626210e52f711d2c2361d102d8d9b8b144e63b2512e748de1a49b')
    version('0.10.1', sha256='263040d2779a3b84930f7ac9da5132be0fefcd6f453a885756656103f8ee1fdd')
    version('0.10.0', sha256='e14070bc84e050e0f80bf6063e31d276f03a0bb4d46b9eca2854566c4ae19837')
    version('0.9.3',  sha256='d8c059dcd81dedb85a9f034d5e22dcb4442c0b201908bede99e306d65ea7c8e7')
    version('0.9.2', sha256='9ec760cbb251c158c19d6c88c17ca00a8632bac713890e465b2be01fdc30713f')

    depends_on('py-setuptools', type='build')
    depends_on('py-cryptography', type=('build', 'run'))
