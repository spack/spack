# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMlflow(PythonPackage):
    """MLflow: A Platform for ML Development and Productionization."""

    homepage = "https://pypi.org/project/mlflow/"
    pypi = "mlflow/mlflow-2.0.1.tar.gz"

    license("Apache-2.0")

    version(
        "2.0.1",
        sha256="3c1e2f20f9a556b099d3b50e0cfdc4577e05c60ad11e5d5fae57122bb1dc7c06",
        url="https://pypi.org/packages/c2/ad/a90f7670677b853f68e7955e6ba4ae9e9ba17aa3ffb638cf7f0d46582e64/mlflow-2.0.1-py3-none-any.whl",
    )
    version(
        "1.17.0",
        sha256="ee0b8bb6a8fab5825a282b0677b6f2f30af508f27582cfe28e6bb701c494e6a1",
        url="https://pypi.org/packages/78/95/66f2e43a3662b27409fdce1775e1fbe8fdb5557140467d9e6654a87cc22e/mlflow-1.17.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2:")
        depends_on("py-alembic", when="@1.28:2.2")
        depends_on("py-alembic@:1.4.1", when="@1.11:1.22")
        depends_on("py-click@7:")
        depends_on("py-cloudpickle@:2", when="@1.28:2.8")
        depends_on("py-cloudpickle", when="@:1.26")
        depends_on("py-databricks-cli@0.8.7:", when="@:2.10.1")
        depends_on("py-docker@4:6", when="@1.29:2.9")
        depends_on("py-docker@4:", when="@:1.26")
        depends_on("py-entrypoints")
        depends_on("py-flask@:2", when="@1.28:2.7")
        depends_on("py-flask", when="@:1.26")
        depends_on("py-gitpython@2.1:", when="@:2.10")
        depends_on("py-gunicorn@:20", when="@1.28:2.5 platform=linux")
        depends_on("py-gunicorn@:20", when="@1.28:2.5 platform=freebsd")
        depends_on("py-gunicorn@:20", when="@1.28:2.5 platform=darwin")
        depends_on("py-gunicorn@:20", when="@1.28:2.5 platform=cray")
        depends_on("py-gunicorn", when="@:1.26 platform=linux")
        depends_on("py-gunicorn", when="@:1.26 platform=freebsd")
        depends_on("py-gunicorn", when="@:1.26 platform=darwin")
        depends_on("py-gunicorn", when="@:1.26 platform=cray")
        depends_on("py-importlib-metadata@3.7:4.6,4.7.1:5", when="@1.30:2.1")
        depends_on("py-jinja2@3.0.0:", when="@2: platform=windows")
        depends_on("py-jinja2@2.11:", when="@2: platform=linux")
        depends_on("py-jinja2@2.11:", when="@2: platform=freebsd")
        depends_on("py-jinja2@2.11:", when="@2: platform=darwin")
        depends_on("py-jinja2@2.11:", when="@2: platform=cray")
        depends_on("py-markdown@3.3:", when="@2:")
        depends_on("py-matplotlib", when="@2.0.0:")
        depends_on("py-numpy@:1", when="@1.28:")
        depends_on("py-numpy", when="@:1.26")
        depends_on("py-packaging@:21", when="@1.28:2.0")
        depends_on("py-pandas@:1", when="@1.28:2.1")
        depends_on("py-pandas", when="@:1.26")
        depends_on("py-prometheus-flask-exporter", when="@:1.26")
        depends_on("py-protobuf@3.12.0:4", when="@1.28:")
        depends_on("py-protobuf@3.6:", when="@:1.17")
        depends_on("py-pyarrow@4:10", when="@2.0.0:2.1")
        depends_on("py-pytz@:2022", when="@1.28:2.2")
        depends_on("py-pytz", when="@1.14:1.26")
        depends_on("py-pyyaml@5.1:", when="@1.28:")
        depends_on("py-pyyaml", when="@:1.17")
        depends_on("py-querystring-parser")
        depends_on("py-requests@2.17.3:")
        depends_on("py-scikit-learn", when="@2:")
        depends_on("py-scipy", when="@1.28:")
        depends_on("py-shap@0.40:", when="@2:2.2")
        depends_on("py-sqlalchemy@1.4.0:1", when="@1.28:2.1")
        depends_on("py-sqlalchemy", when="@1.12:1.26")
        depends_on("py-sqlparse@0.4:", when="@1.28:")
        depends_on("py-sqlparse@0.3.1:", when="@1.12:1.26")
        depends_on("py-waitress@:2", when="@1.28:2.10 platform=windows")
        depends_on("py-waitress", when="@:1.26 platform=windows")
