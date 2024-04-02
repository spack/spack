# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphqlWs(PythonPackage):
    """Websocket backend for GraphQL subscriptions."""

    homepage = "https://github.com/graphql-python/graphql-ws"
    pypi = "graphql-ws/graphql-ws-0.4.4.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "0.4.4",
        sha256="b6f4c9f6968feba80762354068a2a36538a48ac72e4253971be43e0cba020506",
        url="https://pypi.org/packages/97/19/fd64b7972099032bfa88358ad41e95c3348a73661a23727ba2981d43d2af/graphql_ws-0.4.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-graphql-core@2", when="@0.4:")
