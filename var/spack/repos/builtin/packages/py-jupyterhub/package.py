# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterhub(PythonPackage):
    """Multi-user server for Jupyter notebooks."""

    pypi = "jupyterhub/jupyterhub-1.0.0.tar.gz"

    tags = ["e4s"]

    version(
        "1.4.1",
        sha256="20372a507b103a5351bd1dd7782c7524c14b013f43c71d95e37a0efaa9ec6ae9",
        url="https://pypi.org/packages/ac/95/3bb31d8d42aa52f71e713a9027fe3318897f21f76146e7f8843608bb5dbb/jupyterhub-1.4.1-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="e5ba12ba158ffcb1d42ac351f850d0065be14fce012af765cdf30dfe97a7346a",
        url="https://pypi.org/packages/0d/67/c1e7d691bcb635fcde61c544d8fbca1edebb7bb4f68f34f5de291eba02d0/jupyterhub-1.0.0-py3-none-any.whl",
    )
    version(
        "0.9.4",
        sha256="6fd5b19ae152cc637bed2f528ca1bd510042782dc770a32e7ab1ed34e6867873",
        url="https://pypi.org/packages/23/7d/8f272ff69f05d51143e85753939884ca1e578639e273a8bfc1bda69f15bf/jupyterhub-0.9.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-alembic@1.4:", when="@1.4:")
        depends_on("py-alembic", when="@:1.3")
        depends_on("py-async-generator@1.9:", when="@1.3:")
        depends_on("py-async-generator@1.8:", when="@0.9:1.2")
        depends_on("py-certipy@0.1.2:", when="@1:")
        depends_on("py-entrypoints", when="@1:2")
        depends_on("py-jinja2@2.11:", when="@1.3:")
        depends_on("py-jinja2", when="@:1.2")
        depends_on("py-jupyter-telemetry@0.1:", when="@1.2:")
        depends_on("py-oauthlib@3:", when="@1.0.0-beta2:")
        depends_on("py-pamela", when="@1.2.2: platform=linux")
        depends_on("py-pamela", when="@1.2.2: platform=freebsd")
        depends_on("py-pamela", when="@1.2.2: platform=darwin")
        depends_on("py-pamela", when="@1.2.2: platform=cray")
        depends_on("py-pamela", when="@:1.2.1")
        depends_on("py-prometheus-client@0.4:", when="@1.3:")
        depends_on("py-prometheus-client@0.0.21:", when="@0.9:1.2")
        depends_on("py-psutil@5.6.5:", when="@1.1.0: platform=windows")
        depends_on("py-python-dateutil", when="@0.9:")
        depends_on("py-python-oauth2@1:", when="@:0")
        depends_on("py-requests")
        depends_on("py-sqlalchemy@1.1.0:", when="@:3")
        depends_on("py-tornado@5.1:", when="@1.3:")
        depends_on("py-tornado@5.0:", when="@0.9:1.2")
        depends_on("py-traitlets@4.3.2:")
