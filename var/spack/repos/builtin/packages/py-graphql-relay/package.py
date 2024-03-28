# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphqlRelay(PythonPackage):
    """Relay library for graphql-core."""

    homepage = "https://github.com/graphql-python/graphql-relay-py"
    pypi = "graphql-relay/graphql-relay-2.0.1.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "2.0.1",
        sha256="ac514cb86db9a43014d7e73511d521137ac12cf0101b2eaa5f0a3da2e10d913d",
        url="https://pypi.org/packages/94/48/6022ea2e89cb936c3b933a0409c6e29bf8a68c050fe87d97f98aff6e5e9e/graphql_relay-2.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-graphql-core@2.2:2", when="@2")
        depends_on("py-promise@2.2:", when="@2")
        depends_on("py-six@1.12:", when="@2")
