# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAvro(PythonPackage):
    """Avro is a serialization and RPC framework."""

    homepage = "http://avro.apache.org/docs/current/"
    url      = "https://pypi.io/packages/source/a/avro/avro-1.8.2.tar.gz"

    version('1.8.2', '44ec007d432a2f3c35f87eee01f1e9ec')

    depends_on('py-setuptools', type='build')
