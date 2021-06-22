# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "http://spark.apache.org"
    url      = "https://pypi.io/packages/source/p/pyspark/pyspark-2.3.0.tar.gz"

    version('3.1.2', sha256='5e25ebb18756e9715f4d26848cc7e558035025da74b4fc325a0ebc05ff538e65')
    version('3.1.1', sha256='104abc146d4ffb72d4c683d25d7af5a6bf955d94590a76f542ee23185670aa7e')
    version('3.0.0', sha256='8c6e5cc51d91eb8d43e81d0b7093292b5e144ac81445491d5f887d2cf4fe121f')
    version('2.4.5', sha256='0deed5687828efdaf4091e748f0ba1ae8aad6e4c3a5f07aa07e19487397e0e07')
    version('2.4.0', sha256='c9d7b7c5e91b13488b657e364ff392a80b2e374b182138e5ec8702a1822bffdc')
    version('2.3.0', sha256='0b3536910e154c36a94239f0ba0a201f476aadc72006409e5787198ffd01986e')

    depends_on('py-setuptools', type='build')
    depends_on('py-py4j@0.10.9', when='@3.0.0:', type=('build', 'run'))
    depends_on('py-py4j@0.10.7', when='@2.3.0:2.4.99', type=('build', 'run'))

    def setup_run_environment(self, env):
        env.set('PYSPARK_PYTHON', self.spec['python'].command.path)
        env.set('PYSPARK_DRIVER_PYTHON', self.spec['python'].command.path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('PYSPARK_PYTHON', self.spec['python'].command.path)
        env.set('PYSPARK_DRIVER_PYTHON', self.spec['python'].command.path)
