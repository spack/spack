# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySqlalchemyStubs(PythonPackage):
    """
    Mypy plugin and stubs for SQLAlchemy
    """

    homepage = "https://github.com/dropbox/sqlalchemy-stubs"
    pypi = "sqlalchemy-stubs/sqlalchemy-stubs-0.4.tar.gz"

    version(
        "0.4",
        sha256="5eec7aa110adf9b957b631799a72fef396b23ff99fe296df726645d01e312aa5",
        url="https://pypi.org/packages/62/ae/cb215ab25b76228bc90c90444b87e323ffba58c212321a53d5bc92903098/sqlalchemy_stubs-0.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-mypy@0.790:", when="@0.4:")
        depends_on("py-typing-extensions@3.7.4:", when="@0.3:")
