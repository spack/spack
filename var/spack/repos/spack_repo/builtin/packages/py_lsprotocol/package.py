# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLsprotocol(PythonPackage):
    """Code generator and generated types for Language Server Protocol."""

    homepage = "https://github.com/microsoft/lsprotocol"
    pypi = "lsprotocol/lsprotocol-2023.0.1.tar.gz"
    git = "https://github.com/microsoft/lsprotocol.git"

    maintainers("alecbcs")

    license("MIT")

    version("main", branch="main")
    version("2023.0.1", sha256="cc5c15130d2403c18b734304339e51242d3018a05c4f7d0f198ad6e0cd21861d")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-flit-core", type="build")

    depends_on("py-attrs@21.3.0:", type=("build", "run"))
    depends_on("py-cattrs", type=("build", "run"))

    conflicts("^py-cattrs@23.2.1", when="@2023.0.1")
