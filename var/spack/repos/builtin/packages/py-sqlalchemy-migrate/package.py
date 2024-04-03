# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySqlalchemyMigrate(PythonPackage):
    """Database schema migration for SQLAlchemy"""

    homepage = "http://www.openstack.org/"
    pypi = "sqlalchemy-migrate/sqlalchemy-migrate-0.13.0.tar.gz"

    license("MIT")

    version(
        "0.13.0",
        sha256="e5d2348db19a5062132d93e3b4d9e7644af552fffbec4c78cc5358f848d2f6c1",
        url="https://pypi.org/packages/1a/ba/0725bf5f54d0c5ed7c1da025215f288fb68ef4cc4966abfb76c1926ee0af/sqlalchemy_migrate-0.13.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-decorator", when="@0.9.4:")
        depends_on("py-pbr@1.8:", when="@0.11:")
        depends_on("py-six@1.7:", when="@0.9.5:")
        depends_on("py-sqlalchemy@0.9.6:", when="@0.12:")
        depends_on("py-sqlparse", when="@0.9.4:")
        depends_on("py-tempita@0.4:", when="@0.9.4:")
