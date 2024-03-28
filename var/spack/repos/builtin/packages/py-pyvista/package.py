# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyvista(PythonPackage):
    """Easier Pythonic interface to VTK."""

    homepage = "https://github.com/pyvista/pyvista"
    pypi = "pyvista/pyvista-0.32.1.tar.gz"

    # Requires optional trame dependency
    skip_modules = ["pyvista.ext", "pyvista.jupyter", "pyvista.trame"]

    maintainers("banesullivan")

    license("MIT")

    version(
        "0.42.3",
        sha256="b6170689209eec58246b32abb3c5f99246b45948e51228504cda2d4d301e7463",
        url="https://pypi.org/packages/6d/ee/24d100341e673347f80347ec8f20b4e48b1326fd968d7fb1139829f8bb66/pyvista-0.42.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-imageio", when="@0.38")
        depends_on("py-matplotlib@3.0.1:", when="@0.39:")
        depends_on("py-numpy", when="@0.38:0.42")
        depends_on("py-pillow", when="@0.38:")
        depends_on("py-pooch", when="@0.38:")
        depends_on("py-scooby@0.5.1:", when="@0.38:")
        depends_on("py-vtk", when="@0.38:")

    # Historical dependencies

    # '>=3.7.*' in python_requires: setuptools parser changed in v60 and errors.
