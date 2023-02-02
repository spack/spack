# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchtext(PythonPackage):
    """Text utilities and datasets for PyTorch."""

    homepage = "https://github.com/pytorch/text"
    git = "https://github.com/pytorch/text.git"

    maintainers("adamjstewart")

    version("main", branch="main", submodules=True)
    version("0.14.1", tag="v0.14.1", submodules=True)
    version("0.14.0", tag="v0.14.0", submodules=True)
    version("0.13.1", tag="v0.13.1", submodules=True)
    version("0.13.0", tag="v0.13.0", submodules=True)
    version("0.12.0", tag="v0.12.0", submodules=True)
    version("0.11.2", tag="v0.11.2", submodules=True)
    version("0.11.1", tag="v0.11.1", submodules=True)
    version("0.10.1", tag="v0.10.1", submodules=True)
    version("0.10.0", tag="v0.10.0", submodules=True)
    version("0.9.2", tag="v0.9.2", submodules=True)
    version("0.8.1", tag="v0.8.1", submodules=True)
    version("0.6.0", tag="0.6.0", submodules=True)
    version("0.5.0", tag="0.5.0", submodules=True)

    # https://github.com/pytorch/text#installation
    depends_on("python@3.7:3.10", when="@0.13:", type=("build", "link", "run"))
    depends_on("python@3.6:3.9", when="@0.8.1:0.12", type=("build", "link", "run"))
    depends_on("python@3.6:3.8", when="@0.7:0.8.0", type=("build", "link", "run"))
    depends_on("python@3.5:3.8", when="@0.6", type=("build", "link", "run"))
    depends_on("python@2.7,3.5:3.8", when="@:0.5", type=("build", "link", "run"))

    depends_on("cmake@3.18:", when="@0.13:", type="build")
    depends_on("ninja", when="@0.13:", type="build")
    depends_on("py-pybind11", when="@0.8:", type=("build", "link"))
    depends_on("py-setuptools", type="build")
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-six", when="@:0.6", type=("build", "run"))
    depends_on("py-sentencepiece", when="@:0.7", type=("build", "run"))

    # https://github.com/pytorch/text#installation
    depends_on("py-torch@master", when="@main", type=("build", "link", "run"))
    depends_on("py-torch@1.13.1", when="@0.14.1", type=("build", "link", "run"))
    depends_on("py-torch@1.13.0", when="@0.14.0", type=("build", "link", "run"))
    depends_on("py-torch@1.12.1", when="@0.13.1", type=("build", "link", "run"))
    depends_on("py-torch@1.12.0", when="@0.13.0", type=("build", "link", "run"))
    depends_on("py-torch@1.11.0", when="@0.12.0", type=("build", "link", "run"))
    depends_on("py-torch@1.10.2", when="@0.11.2", type=("build", "link", "run"))
    depends_on("py-torch@1.10.1", when="@0.11.1", type=("build", "link", "run"))
    depends_on("py-torch@1.9.1", when="@0.10.1", type=("build", "link", "run"))
    depends_on("py-torch@1.9.0", when="@0.10.0", type=("build", "link", "run"))
    depends_on("py-torch@1.8.2", when="@0.9.2", type=("build", "link", "run"))
    depends_on("py-torch@1.7.1", when="@0.8.1", type=("build", "link", "run"))
    depends_on("py-torch@1.5.0", when="@0.6.0", type=("build", "link", "run"))
    depends_on("py-torch@1.4.1", when="@0.5.0", type=("build", "link", "run"))
