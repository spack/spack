# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyToolUtil(PythonPackage):
    """The Galaxy tool utilities."""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-tool-util/galaxy-tool-util-22.1.5.tar.gz"

    license("CC-BY-3.0")

    version(
        "22.1.5",
        sha256="062a758024cda103d3d40ba232379c0c1853e8e181b58a65c4e954456cdcc040",
        url="https://pypi.org/packages/76/b0/4745ccb75fdb5c48a27a73900f8430119afe6c7c95b1aafed004f093788c/galaxy_tool_util-22.1.5-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-galaxy-containers@22:", when="@22.1.2:22.1")
        depends_on("py-galaxy-util@22:", when="@22.1.2:")
        depends_on("py-lxml")
        depends_on("py-pydantic", when="@21.9:23.0.3")
        depends_on("py-pyyaml", when="@22:")
        depends_on("py-sortedcontainers", when="@21.9:")
        depends_on("py-typing-extensions", when="@21.9:")
