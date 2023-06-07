# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyomo(PythonPackage):
    """Pyomo is a Python-based open-source software package that supports a
    diverse set of optimization capabilities for formulating and analyzing
    optimization models."""

    homepage = "http://www.pyomo.org/"
    pypi = "Pyomo/Pyomo-5.6.6.tar.gz"
    git = "https://github.com/Pyomo/pyomo.git"

    # Maintainer accurate as of 06/06/2023
    maintainers("mrmundt")

    version("6.6.1", sha256="e24d7a600972f9d1150eeec520d759153b2c2d433c2f318a4dc6a985573e727a")
    version("6.6.0", sha256="fbf6f3bf093387d8eaf8f2f824821b59380b28933298552f8dc178d98a8b9bd3")
    version("6.5.0", sha256="8a531fc372e2723c942fb7e4c201f13615100acee460d5748c16a2306813f29b")
    version("6.4.4", sha256="0c45b0fdfc1e823007bbc3a9a153e90ca9f0b264ef229b1b9314aac286e6f91a")
    version("6.4.3", sha256="143f375c307a1b6f161fcd8b2ffb06b4045f6009449d824a59680c567763b1f4")
    version("6.4.2", sha256="f0af50ca40f19a1522c00531384ca21dcb0c2bcb2bcbc05c381a292ed23796e4")
    version("6.4.1", sha256="d9895443d11739ea9826a2147585f158a95f16517a078d1966f395bb78a6c04d")
    version("6.4.0", sha256="9f2d7615c002da80feea9d66bebcb0441befa092c29ed4515fce8118870d8ff4")
    version("6.3.0", sha256="39ed09cfdb77bf2e44cc8d4461bce68fc48a04bf582666b6b1cc89997806a969")
    version("6.2", sha256="c123a4cde0b74a40f984e56829decbae23f41760c829e79344001e8b0bbf2eb9")
    version("6.1.2", sha256="b295c99bdb0e8b5329b7f5e56edcdd59edc8f8bae6c01888243b59c9ff651628")
    version("6.1.1", sha256="7e034d98b0a6a7a5aa84c7e6ebfd87df1f7807c9e01e51e5c663c615637dd37a")
    version("6.1", sha256="850e6e779ba4e7a144bba29e93d591b6859d7bd12848202507c8bc68f8128191")
    version("6.0.1", sha256="c3ab4064c3f8c5c8927d7e01306059551c26b934280d4052fefeb922ef5b064d")
    version("6.0", sha256="5c41ce1f6cd0725981d18c3da6986a5412e0da2bfa50701582de9795ff73fb34")
    version("5.7.3", sha256="991bf4f14a9ce36333e8f00dae50ea8c4e30cbc04fdbd1b87c703e68a8ceb0c8")
    version("5.7.2", sha256="806106471350277d29adb41f2b51624fe31d8afca9fecb884b669c38888d09f0")
    version("5.7.1", sha256="790ae4bb208b415e16ff679ea35d4a49c58f164af78ffa5993e15a83949f7371")
    version("5.7.0", sha256="56bd8b36e7ccc3365725b281518b666a425adbfc803c2ddcb270715283358d49")
    version("5.6.9", sha256="8d6637925d1e37a9b489179f0e2faf21d2b68e5fffc3452ec3964474fb8a51cb")
    version("5.6.8", sha256="34bba5dea8eb0b827e486cf15a5f462eced79a412e30f5aa1423d9842d18f9f0")
    version("5.6.7", sha256="04e1be62c384c8605f840c7e71753266473ec2254552831dd5622ba09d966e5b")
    version("5.6.6", sha256="9330956b9fb244351ce76aaaf88688b5bdd03eebb122020cbee7b46e198a4110")

    variant("cython", default=False, description="Enable cythonization of Pyomo.")
    variant("tests", default=False, description="Install testing dependencies. (Version 6.1+)")
    variant("docs", default=False, description="Install docs generation dependencies. (Version 6.1+)")
    variant("optional", default=False, description="Install optional dependencies. (Version 6.1+)")

    # python_requires
    depends_on("python@3.7:3.11", when="@6.4:", type=("build", "run"))
    depends_on("python@3.6:3.10", when="@6.3", type=("build", "run"))
    depends_on("python@3.6:3.9", when="@6.0:6.2", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:3.9", when="@5.7", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:3.8", when="@5.6", type=("build", "run"))

    # universally required
    depends_on("py-setuptools", type="build")
    depends_on("py-ply", type=("build", "run"))

    # required for pre-6 series
    depends_on("py-pyutilib@6.0.0", when="@5", type=("build", "run"))
    depends_on("py-six@1.4:", when="@5", type=("build", "run"))
    depends_on("py-appdirs", when="@5.6:5.7.0", type=("build", "run"))
    depends_on("py-enum34", when="@5.7:", type=("build", "run"))

    # when cython is requested
    depends_on("py-cython", when="+cython", type="build")

    # when tests is requested
    depends_on("py-coverage", when="@6.1:+tests", type=("build", "run"))
    depends_on("py-nose", when="@6.1:6.2+tests", type=("build", "run"))
    depends_on("py-pytest", when="@6.3:+tests", type=("build", "run"))
    depends_on("py-pytest-parallel", when="@6.3:+tests", type=("build", "run"))
    depends_on("py-parameterized", when="@6.1:+tests", type=("build", "run"))
    depends_on("py-pybind11", when="@6.1:+tests", type=("build", "run"))

    # when docs is requested
    depends_on("py-sphinx@2:", when="@6.1:+docs", type=("build", "run"))
    depends_on("py-sphinx-copybutton", when="@6.1:+docs", type=("build", "run"))
    depends_on("py-sphinx-rtd-theme@0.5:", when="@6.1:+docs", type=("build", "run"))
    depends_on("py-sphinxcontrib-jsmath", when="@6.1:+docs", type=("build", "run"))
    depends_on("py-sphinxcontrib-napoleon", when="@6.1:+docs", type=("build", "run"))
    depends_on("py-numpy", when="@6.1:+docs", type=("build", "run"))
    depends_on("py-scipy", when="@6.4.2:+docs", type=("build", "run"))

    # when optional is requested
    depends_on("py-dill", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-ipython", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-matplotlib@3.6.2:", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-networkx", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-numpy", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-openpyxl", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-pint", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-python-louvain", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-pyyaml", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-scipy", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-sympy", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-xlrd", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-pandas", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-seaborn", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-numdifftools", when="@6.1:+optional", type=("build", "run"))
    depends_on("py-plotly", when="@6.6:+optional", type=("build", "run"))


    def global_options(self, spec, prefix):
        options = []
        if "+cython" in self.spec:
            options.append("--with-cython")
        return options
