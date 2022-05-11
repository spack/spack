# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyPika(PythonPackage):
    """Pika is a RabbitMQ (AMQP 0-9-1) client library for Python."""

    homepage = 'https://pika.readthedocs.io/'
    git      = 'https://github.com/pika/pika.git'
    pypi     = 'pika/pika-1.2.0.tar.gz'

    version('1.2.0',  sha256='f023d6ac581086b124190cb3dc81dd581a149d216fa4540ac34f9be1e3970b89')
    version('1.1.0',  sha256='9fa76ba4b65034b878b2b8de90ff8660a59d925b087c5bb88f8fdbb4b64a1dbf')
    version('1.0.0',  sha256='fba41293b35c845bd96cfdd29981f0eeff91f705ac0c3ba361a771c4bfbc3485')
    version('0.13.1', sha256='b0640085f1d6398fd47bb16a17713053e26578192821ea5d928772b8e6a28789')
    version('0.13.0', sha256='5338d829d1edb3e5bcf1523b4a9e32c56dea5a8bda7018825849e35325580484')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',   type='build')
