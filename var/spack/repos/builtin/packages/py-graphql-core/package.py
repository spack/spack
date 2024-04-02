# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGraphqlCore(PythonPackage):
    """GraphQL-core 3 is a Python 3.6+ port of GraphQL.js, the
    JavaScript reference implementation for GraphQL, a query language
    for APIs created by Facebook."""

    homepage = "https://github.com/graphql-python/graphql-core"
    pypi = "graphql-core/graphql-core-3.1.5.tar.gz"

    license("MIT")

    version(
        "3.1.2",
        sha256="b1826fbd1c6c290f7180d758ecf9c3859a46574cff324bf35a10167533c0e463",
        url="https://pypi.org/packages/8b/04/5f79f6c48383d40717867bfcbda72adfeff20bb5dcc14abe7d44edf7064d/graphql_core-3.1.2-py3-none-any.whl",
    )
    version(
        "3.0.5",
        sha256="dfc374d3426677727772d8da9dd010e92d10305ddd9c2f7f0fc388f07cee94c4",
        url="https://pypi.org/packages/cc/45/c74fe65ade57473105f727ae9c8c36b8cf5b592d88ffae9b8b3198cd52c2/graphql_core-3.0.5-py3-none-any.whl",
    )
    version(
        "2.3.2",
        sha256="44c9bac4514e5e30c5a595fac8e3c76c1975cae14db215e8174c7fe995825bad",
        url="https://pypi.org/packages/11/71/d51beba3d8986fa6d8670ec7bcba989ad6e852d5ae99d95633e5dacc53e7/graphql_core-2.3.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@3:3.2")
        depends_on("py-promise@2.3:", when="@2.3:2")
        depends_on("py-rx@1.6:1", when="@2.3:2")
        depends_on("py-six@1.10:", when="@:2")
