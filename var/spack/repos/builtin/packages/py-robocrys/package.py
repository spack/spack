# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRobocrys(PythonPackage):
    """Robocrystallographer is a tool to generate text descriptions of crystal
    structures. Similar to how a real-life crystallographer would analyse a
    structure, robocrystallographer looks at the symmetry, local environment, and
    extended connectivity when generating a description. The package includes
    utilities for identifying molecule names, component orientations, heterostructure
    information, and more."""

    homepage = "https://github.com/hackingmaterials/robocrystallographer"
    pypi = "robocrys/robocrys-0.2.7.tar.gz"

    maintainers("meyersbs")

    version(
        "0.2.7",
        sha256="5caafe816c68a2d2d2446f3774d0ec9853bc4e7d91d8907fa71b9cdf4ee9d5c9",
        url="https://pypi.org/packages/40/62/f3c599e6533e5f43f759478c642327fc195938ee1be9e053b0288031504f/robocrys-0.2.7-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.2.7")
        depends_on("py-inflect", when="@:0.2.4,0.2.6:")
        depends_on("py-matminer", when="@:0.1,0.2.6:")
        depends_on("py-monty", when="@:0.2.4,0.2.6:")
        depends_on("py-networkx", when="@:0.2.4,0.2.6:")
        depends_on("py-numpy", when="@:0.2.4,0.2.6:")
        depends_on("py-pubchempy", when="@:0.2.4,0.2.6:")
        depends_on("py-pybtex", when="@:0.2.4,0.2.6:")
        depends_on("py-pymatgen@2020.10.20:", when="@0.2.6:")
        depends_on("py-ruamel-yaml", when="@0.2.7:")
        depends_on("py-scipy", when="@:0.2.4,0.2.6:")
        depends_on("py-spglib", when="@:0.2.4,0.2.6:")
