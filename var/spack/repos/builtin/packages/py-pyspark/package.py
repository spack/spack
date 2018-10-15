# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "http://spark.apache.org"
    url      = "https://pypi.org/packages/source/p/pyspark/pyspark-2.3.0.tar.gz"

    version('2.3.2rc2',
            url='https://github.com/matz-e/bbp-spark/releases/download/v2.3.2-rc2/pyspark-2.3.2-rc2-patched.tgz',
            sha256='45c6ba87543009843c134b73e56510b936b7b130ee22c116263f8ebe32fdfa59')
    version('2.3.0', sha256='0b3536910e154c36a94239f0ba0a201f476aadc72006409e5787198ffd01986e')

    depends_on('py-setuptools', type='build')
    depends_on('py-py4j', type=('build', 'run'))
