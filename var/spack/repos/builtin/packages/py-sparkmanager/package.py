##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PySparkmanager(PythonPackage):
    """Small shim to manage Spark in a more convenient way"""

    homepage = "https://github.com/matz-e/sparkmanager"
    url      = "https://pypi.org/packages/source/s/sparkmanager/sparkmanager-0.6.0.tar.gz"

    version('0.7.3', sha256='bf952e31d9fc6c4945613caae64558625b792596985920bcd4c5fa8b73a97a78')
    version('0.7.0', sha256='5858728b8c91597970293c26b2f114161a435527a5600f9a7386f4e6d28ec7d9')
    version('0.6.0', sha256='98aa542942690b533f087fab1b5544abe189c4f4ee3e16b65f12f5758671db54')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pyspark', type=('build', 'run'))
    depends_on('spark', type='run')
