# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAbipy(PythonPackage):
    """Python package to automate ABINIT calculations and analyze
    the results."""

    homepage = "https://github.com/abinit/abipy"
    pypi = "abipy/abipy-0.2.0.tar.gz"

    version(
        "0.9.3",
        sha256="c8102dbcea012d6e8d53eccbe62e4d84411e5cd136493fe6ffdd40d1f0248ca5",
        url="https://pypi.org/packages/e9/3d/9b0722eb114fa3052266f998b5456c4d25eb50d347c65e222be687007228/abipy-0.9.3-py2.py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="3d2cc9c40ef3998684067e78817ea1d936562fe77f1d333c2dc187450ff64dda",
        url="https://pypi.org/packages/58/d9/35e46e22871757769d79cffbd31f1b53d0bcc65658d3c2bb3fea03672cbe/abipy-0.2.0-py27-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-apscheduler", when="@0.9:0.9.6")
        depends_on("py-apscheduler@2.1:2.1.0", when="@:0.3,0.5:0.6,0.8")
        depends_on("py-chart-studio", when="@0.9.1:")
        depends_on("py-html2text", when="@:0.3,0.5:0.6")
        depends_on("py-ipython", when="@0.9.1:")
        depends_on("py-matplotlib", when="@0.3,0.5:0.6,0.8:")
        depends_on("py-matplotlib@1.5:", when="@:0.2")
        depends_on("py-monty", when="@0.8:")
        depends_on("py-netcdf4", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-numpy", when="@0.3,0.5:0.6,0.8:")
        depends_on("py-numpy@1.9:", when="@:0.2")
        depends_on("py-pandas", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-plotly", when="@0.9.1:")
        depends_on("py-prettytable", when="@:0.3,0.5")
        depends_on("py-pydispatcher@2.0.5:", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-pymatgen@2022.0.14:", when="@0.9.2:")
        depends_on("py-pymatgen@4.7.2:", when="@:0.2")
        depends_on("py-pyyaml@3.11:", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-scipy", when="@0.3,0.5:0.6,0.8:")
        depends_on("py-scipy@0.14:", when="@:0.2")
        depends_on("py-seaborn", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-six", when="@:0.3,0.5:0.6")
        depends_on("py-spglib", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-tabulate", when="@:0.3,0.5:0.6,0.8:")
        depends_on("py-tqdm", when="@:0.3,0.5:0.6,0.8:")
