# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyvista(PythonPackage):
    """Easier Pythonic interface to VTK."""

    homepage = "https://github.com/pyvista/pyvista"
    pypi = "pyvista/pyvista-0.32.1.tar.gz"

    maintainers("banesullivan")

    version("0.37.0", sha256="d36a2c6d5f53f473ab6a9241669693acee7a5179394dc97595da14cc1de23141")
    version("0.32.1", sha256="585ac79524e351924730aff9b7207d6c5ac4175dbb5d33f7a9a2de22ae53dbf9")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-imageio", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-pooch", when="@0.37:", type=("build", "run"))
    depends_on("py-scooby@0.5.1:", type=("build", "run"))
    depends_on("vtk+python", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))

    # Historical dependencies
    depends_on("py-appdirs", when="@:0.36", type=("build", "run"))
    depends_on("py-meshio@4.0.3:4", when="@:0.32", type=("build", "run"))
