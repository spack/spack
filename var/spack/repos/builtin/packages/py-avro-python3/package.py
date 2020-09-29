# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAvroPython3(PythonPackage):
    """Apache Avro™ is a data serialization system."""

    homepage = "https://github.com/apache/avro/tree/master/lang/py3"
    url      = "https://pypi.io/packages/source/a/avro-python3/avro-python3-1.10.0.tar.gz"

    version('1.10.0', sha256='a455c215540b1fceb1823e2a918e94959b54cb363307c97869aa46b5b55bde05')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
