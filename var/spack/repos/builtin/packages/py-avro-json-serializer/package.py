# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAvroJsonSerializer(PythonPackage):
    """Serializes data into a JSON format using AVRO schema."""

    homepage = "https://github.com/linkedin/python-avro-json-serializer"
    url      = "https://github.com/linkedin/python-avro-json-serializer/archive/0.4.tar.gz"

    version('0.4',  sha256='58df57e6c85b1b453668eb0bff2b049efcfd83d6e5dfa72cee1df220f330820d')

    depends_on('py-setuptools', type='build')
    depends_on('py-simplejson', type=('build', 'run'))
    depends_on('py-avro', type=('build', 'run'))
