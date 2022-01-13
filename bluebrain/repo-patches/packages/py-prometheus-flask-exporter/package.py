# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPrometheusFlaskExporter(PythonPackage):
    """Prometheus metrics exporter for Flask."""

    homepage = "https://pypi.org/project/prometheus-flask-exporter/"
    url = "https://files.pythonhosted.org/packages/f3/c1/2cc385fadf18dc75fe24c18899269eda4dcc60221d61eff7da4a6cc5c01d/prometheus_flask_exporter-0.18.2.tar.gz"

    version('0.18.2', sha256='fc487e385d95cb5efd045d6a315c4ecf68c42661e7bfde0526af75ed3c4f8c1b')

    depends_on('py-setuptools', type='build')
    depends_on('py-prometheus-client', type=('run'))
    depends_on('py-flask', type=('run'))
