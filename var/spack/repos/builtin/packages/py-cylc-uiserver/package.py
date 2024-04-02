# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcUiserver(PythonPackage):
    """Cylc UI Server."""

    homepage = "https://github.com/cylc/cylc-uiserver/"
    pypi = "cylc-uiserver/cylc-uiserver-1.3.0.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0-or-later")

    version(
        "1.3.0",
        sha256="80cb1dd667a140475353ac81c27bc5bcc10d60cbcfe699224dd177837903775f",
        url="https://pypi.org/packages/20/00/baeab533e75fe3f9e17a0c25d10687111de4b8d7f76afbd5075730029138/cylc_uiserver-1.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1:1.3")
        depends_on("py-ansimarkup@1:", when="@1.2.1:")
        depends_on("py-cylc-flow@8.2:", when="@1.3:")
        depends_on("py-graphene", when="@1:")
        depends_on("py-graphene-tornado@2.6:2", when="@0.2:")
        depends_on("py-graphql-core", when="@1:")
        depends_on("py-graphql-ws@0.4.4:", when="@1:")
        depends_on("py-jupyter-server@1.10.2:1", when="@1.3")
        depends_on("py-pyzmq", when="@1:")
        depends_on("py-requests", when="@1.2.2:")
        depends_on("py-rx@:1", when="@1:")
        depends_on("py-tornado@6.1:", when="@1:")
        depends_on("py-traitlets@5.2.1:", when="@1:")
