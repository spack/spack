# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGql(PythonPackage):
    """This is a GraphQL client for Python. Plays nicely with
    graphene, graphql-core, graphql-js and any other GraphQL
    implementation compatible with the spec.
    GQL architecture is inspired by React-Relay and Apollo-Client."""

    homepage = "https://github.com/graphql-python/gql"
    pypi = "gql/gql-2.0.0.tar.gz"

    license("MIT")

    version(
        "3.0.0-alpha1",
        sha256="167479b3ade9774ab51e843d38ae372d0fa7267241bc42f50ea2d976217d4ea5",
        url="https://pypi.org/packages/41/d4/73ed61ce0d31a04b0bc1680cf8993327f8708daab1d7376e231833ca9c92/gql-3.0.0a1-py2.py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="6ecbb91ec321f867b3c4a9ddd9bab09f7eacffd8c0f86b3bda7809b6feee3f95",
        url="https://pypi.org/packages/10/c8/e95460fb9b64f7aede3a3c8f6076b54c9ece66c5f790f3bf3345460ddeaf/gql-0.4.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-aiohttp@3.6.2", when="@3:3.0.0-alpha1")
        depends_on("py-graphql-core@3.1.0:3.1", when="@3:3.0.0-alpha1")
        depends_on("py-requests@2.23:", when="@3:3.0.0-alpha1")
        depends_on("py-websockets@8.1:8", when="@3:3.0.0-alpha1")
        depends_on("py-yarl@1.4.0:", when="@3:3.0.0-alpha1")
