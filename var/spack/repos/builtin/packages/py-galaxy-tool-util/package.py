# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyToolUtil(PythonPackage):
    """The Galaxy tool utilities."""

    homepage = "https://github.com/galaxyproject/galaxy"

    version(
        "22.1.5",
        url="https://files.pythonhosted.org/packages/76/b0/4745ccb75fdb5c48a27a73900f8430119afe6c7c95b1aafed004f093788c/galaxy_tool_util-22.1.5-py2.py3-none-any.whl",
        sha256="062a758024cda103d3d40ba232379c0c1853e8e181b58a65c4e954456cdcc040",
        expand=False,
    )

    depends_on("python@3.7:3.10", type=("build", "run"))
    depends_on("py-setuptools", type="build")
