# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAbipy(PythonPackage):
    """Python package to automate ABINIT calculations and analyze
    the results."""

    homepage = "https://github.com/abinit/abipy"
    pypi = "abipy/abipy-0.2.0.tar.gz"

    version("0.9.3", sha256="2f750c1ddcf78d0ec77c1bd44624ff96f80436307237589c02da127106514b75")
    version("0.2.0", sha256="c72b796ba0f9ea4299eac3085bede092d2652e9e5e8074d3badd19ef7b600792")

    variant("gui", default=False, description="Build the GUI")
    variant("ipython", default=False, when="0.2.0", description="Build IPython support")

    depends_on("py-setuptools", type="build")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build", when="+ipython")

    depends_on("py-monty", type=("build", "run"), when="@0.7:")
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-apscheduler", type=("build", "run"), when="@0.9:")
    depends_on("py-apscheduler@2.1.0", type=("build", "run"), when="@:0.8")
    depends_on("py-pydispatcher@2.0.5:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pyyaml@3.11:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-numpy@1.9:", type=("build", "run"), when="@0.2.0")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scipy@0.14:", type=("build", "run"), when="@0.2.0")
    depends_on("py-spglib", type=("build", "run"))
    depends_on("py-pymatgen@2022.0.14:", type=("build", "run"), when="@0.9.2:")
    depends_on("py-pymatgen@4.7.2:", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-matplotlib@1.5:", type=("build", "run"), when="@0.2.0")
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-plotly", type=("build", "run"), when="@0.9.1:")
    depends_on("py-ipython", type=("build", "run"), when="@0.9.1:")
    depends_on("py-chart-studio", type=("build", "run"), when="@0.9.1:")

    with when("+gui"):
        depends_on("py-wxpython", type=("build", "run"))
        depends_on("py-wxmplot", type=("build", "run"))

    with when("+ipython"):
        depends_on("py-ipython", type=("build", "run"))
        depends_on("py-jupyter", type=("build", "run"))
        depends_on("py-nbformat", type=("build", "run"))

    # Historical dependencies
    depends_on("py-six", type=("build", "run"), when="@:0.6")
    depends_on("py-html2text", type=("build", "run"), when="@:0.6")
    depends_on("py-prettytable", type=("build", "run"), when="@:0.5")

    @when("0.2.0")
    def install_options(self, spec, prefix):
        args = []

        if "+ipython" in spec:
            args.append("--with-ipython")

        return args

    @property
    def skip_modules(self):
        modules = []

        if self.spec.satisfies("~gui"):
            modules.append("abipy.gui")

        return modules
