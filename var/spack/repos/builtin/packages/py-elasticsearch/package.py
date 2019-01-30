# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyElasticsearch(PythonPackage):
    """Python client for Elasticsearch"""

    homepage = "https://github.com/elastic/elasticsearch-py"
    url = "https://pypi.io/packages/source/e/elasticsearch/elasticsearch-5.2.0.tar.gz"

    version('5.2.0', '66692fd1b4189039206c2fde4a4d616a')
    version('2.3.0', '2550f3b51629cf1ef9636608af92c340')

    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.8:1.999', type=('build', 'run'))
    # tests_require
    # depends_on('py-requests@1.0.0:2.9.999', type=('build', 'run'))
    # depends_on('py-nose', type=('build', 'run'))
    # depends_on('py-coverage', type=('build', 'run'))
    # depends_on('py-mock', type=('build', 'run'))
    # depends_on('py-pyyaml', type=('build', 'run'))
    # depends_on('py-nosexcover', type=('build', 'run'))
