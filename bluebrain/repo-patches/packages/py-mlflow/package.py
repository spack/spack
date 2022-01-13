# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMlflow(PythonPackage):
    """MLflow: A Platform for ML Development and Productionization."""

    homepage = "https://pypi.org/project/mlflow/"
    url = "https://files.pythonhosted.org/packages/70/3d/277ebf830476a6d320ce1439522ff65c705784517c00f77f9e20c0fae8b6/mlflow-1.17.0.tar.gz"

    version('1.17.0', sha256='4898c58899e3101e09e2b37cf5bee7db04c5d73389a56942d3ef5a5e4396799e')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-click@7.0:', type=('run'))
    depends_on('py-cloudpickle', type=('run'))
    depends_on('py-databricks-cli@0.8.7:', type=('run'))
    depends_on('py-entrypoints', type=('run'))
    depends_on('py-gitpython@2.1.0:', type=('run'))
    depends_on('py-pyyaml', type=('run'))
    depends_on('py-protobuf@3.6.0:', type=('run'))
    depends_on('py-pytz', type=('run'))
    depends_on('py-requests@2.17.3:', type=('run'))
    depends_on('py-alembic@:1.4.1', type=('run'))
    depends_on('py-docker@4.0.0:', type=('run'))
    depends_on('py-flask', type=('run'))
    depends_on('py-gunicorn', type=('run'))
    depends_on('py-numpy', type=('run'))
    depends_on('py-pandas', type=('run'))
    depends_on('py-prometheus-flask-exporter', type=('run'))
    depends_on('py-querystring-parser', type=('run'))
    depends_on('py-sqlparse@0.3.1:', type=('run'))
    depends_on('py-sqlalchemy', type=('run'))
