# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabPygments(PythonPackage):
    """Pygments theme using JupyterLab CSS variables."""

    homepage = "https://jupyter.org/"
    pypi = "jupyterlab-pygments/jupyterlab_pygments-0.1.1.tar.gz"

    version("0.2.2", sha256="7405d7fde60819d905a9fa8ce89e4cd830e318cdad22a0030f7a901da705585d")
    version("0.1.2", sha256="cfcda0873626150932f438eccf0f8bf22bfa92345b814890ab360d666b254146")
    version("0.1.1", sha256="19a0ccde7daddec638363cd3d60b63a4f6544c9181d65253317b2fb492a797b9")

    depends_on("python@3.7:", when="@0.2.2:", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.1.2", type="build")
    depends_on("py-jupyter-packaging11", when="@0.2.2:", type="build")
    depends_on("py-jupyterlab@3.1:3", when="@0.2.2:", type="build")
    depends_on("py-pygments@2.4.1:2", type=("build", "run"))
