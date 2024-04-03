# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskSqlalchemy(PythonPackage):
    """
    Add SQLAlchemy support to your Flask application.
    """

    homepage = "https://github.com/pallets-eco/flask-sqlalchemy"
    pypi = "flask-sqlalchemy/Flask-SQLAlchemy-3.0.2.tar.gz"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    version(
        "3.0.2",
        sha256="7d0cd9cf73e64a996bb881a1ebd01633fc5a6d11c36ea27f7b5e251dc45476e7",
        url="https://pypi.org/packages/1b/9c/2b3ce12b3f7eca00d1f54a6eb84e6cb57b628aa2891a81bb12dfd8b6d604/Flask_SQLAlchemy-3.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3:3.0")
        depends_on("py-flask@2.2:", when="@3.0.0:3.0.3")
        depends_on("py-sqlalchemy@1.4.18:", when="@3.0.0:3.0")

    # https://github.com/pallets-eco/flask-sqlalchemy/blob/3.0.2/pyproject.toml
