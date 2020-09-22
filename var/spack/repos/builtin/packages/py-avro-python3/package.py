# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAvroPython3(PythonPackage):
    """Apache Avro™ is a data serialization system."""

    homepage = "https://github.com/apache/avro/tree/master/lang/py3"
    url      = "https://files.pythonhosted.org/packages/b2/5a/819537be46d65a01f8b8c6046ed05603fb9ef88c663b8cca840263788d58/avro-python3-1.10.0.tar.gz"

    version('1.10.0', sha256='a455c215540b1fceb1823e2a918e94959b54cb363307c97869aa46b5b55bde05')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
