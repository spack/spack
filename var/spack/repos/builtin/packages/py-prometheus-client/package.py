# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPrometheusClient(PythonPackage):
    """Prometheus instrumentation library for Python applications."""

    homepage = "https://github.com/prometheus/client_python"
    url      = "https://github.com/prometheus/client_python/archive/v0.5.0.tar.gz"

    version('0.5.0', sha256='2d7f7af343dec0a96ee849b1bba18aad9f767bf16d5eb5f0c11cae837bf22731')

    depends_on('py-setuptools', type='build')
