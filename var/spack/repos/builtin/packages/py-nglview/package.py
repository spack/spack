# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNglview(PythonPackage):
    """Jupyter widget to interactively view molecular structures and trajectories."""

    homepage = "http://nglviewer.org"
    pypi = "nglview/nglview-3.1.1.tar.gz"

    version("3.1.1", sha256="71c61a69c2d459ee93b40698fa54ad9cc793003d3dbbbb520e9a61975813c1cd")

    depends_on("py-ipywidgets@8:", type="run")
    depends_on("py-jupyterlab-widgets", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-notebook@7:", type="run")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@40.8.0:", type="build")
    depends_on("py-jupyter-packaging@0.7:", type="build")
    depends_on("py-versioneer", type="build")
