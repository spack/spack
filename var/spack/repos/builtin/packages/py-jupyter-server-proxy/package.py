# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServerProxy(PythonPackage):
    """
    Jupyter Server Proxy lets you run arbitrary external processes
    (such as RStudio, Shiny Server, Syncthing, PostgreSQL, Code Server, etc)
    alongside your notebook server and provide authenticated web access to them
    using a path like /rstudio next to others like /lab.
    """

    homepage = "https://github.com/jupyterhub/jupyter-server-proxy"
    pypi = "jupyter-server-proxy/jupyter-server-proxy-3.2.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.2.2",
        sha256="9420814a2f0ef629bd343b4f4e971d6a5ebceb56eabefd6ba03f590fe698cb82",
        url="https://pypi.org/packages/53/e6/35f9cf3fea354aa2befae9f34534e3312f0d719361585a5ada3ced3f73f8/jupyter_server_proxy-3.2.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-aiohttp")
        depends_on("py-jupyter-server@1.0.0:", when="@3.0.0:")
        depends_on("py-simpervisor@0.4:", when="@1.5.3:4.0")
