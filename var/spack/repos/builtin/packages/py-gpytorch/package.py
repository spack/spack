# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGpytorch(PythonPackage):
    """GPyTorch is a Gaussian process library implemented using PyTorch.
    GPyTorch is designed for creating scalable, flexible, and modular Gaussian
    process models with ease."""

    homepage = "https://gpytorch.ai/"
    pypi = "gpytorch/gpytorch-1.2.1.tar.gz"

    maintainers("adamjstewart", "meyersbs")

    version("1.10", sha256="6dc978ab9fbf220a845a4f1ea13104180fc50e6934081f421b37f6120afb7f18")
    version("1.9.1", sha256="0bdbba6f6d5957a0f43ef6dc7fec39c47e8a55f632ca33760c6189f259b3ccc3")
    version("1.9.0", sha256="a0608184c18a1f518d6a102473427abf00f5351421e12a934530953f6887b34b")
    version("1.8.1", sha256="fe8e412a73a2b07027e30c65c61323de15ebcef439f5bd21200cf26551fd0e30")
    version("1.8.0", sha256="d6c0c77d9a61f47feac2d19456816ccea1ed48c32c72d7ea33aa13b259e2a455")
    version("1.7.0", sha256="e91cb8a1883d54f8f57cebbc0c61c227b3cd72528d8e90e770f971fc4e408538")
    version("1.6.0", sha256="08e8f1a80669dc3eee5ba237fc00c867a8858f9b186bbec8571a8cf9af36f543")
    version("1.2.1", sha256="ddd746529863d5419872610af23b1a1b0e8a29742131c9d9d2b4f9cae3c90781")
    version("1.2.0", sha256="fcb216e0c1f128a41c91065766508e91e487d6ffadf212a51677d8014aefca84")
    version("1.1.1", sha256="76bd455db2f17af5425f73acfaa6d61b8adb1f07ad4881c0fa22673f84fb571a")

    depends_on("python@3.8:", when="@1.9:", type=("build", "run"))
    depends_on("python@3.7:", when="@1.7:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", when="@1.9:", type="build")
    depends_on("py-torch@1.11:", when="@1.9:", type=("build", "run"))
    depends_on("py-torch@1.10:", when="@1.7:", type=("build", "run"))
    depends_on("py-torch@1.9:", when="@1.6:", type=("build", "run"))
    depends_on("py-torch@1.8.1:", when="@1.5:", type=("build", "run"))
    depends_on("py-torch@1.7:", when="@1.3:", type=("build", "run"))
    depends_on("py-torch@1.6:", when="@1.2:", type=("build", "run"))
    depends_on("py-torch@1.5:", type=("build", "run"))
    depends_on("py-scikit-learn", when="@1.2:", type=("build", "run"))
    depends_on("py-linear-operator@0.1.1:", when="@1.9:", type=("build", "run"))
    depends_on("py-linear-operator@0.2.0:", when="@1.9.1:", type=("build", "run"))
    depends_on("py-linear-operator@0.4.0:", when="@1.10:", type=("build", "run"))
    depends_on("py-numpy", when="@1.7:1.8", type=("build", "run"))
    depends_on("py-scipy", when="@1.2:1.8", type=("build", "run"))
