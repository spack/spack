# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchtext(PythonPackage):
    """Text utilities, models, transforms, and datasets for PyTorch."""

    homepage = "https://github.com/pytorch/text"
    git = "https://github.com/pytorch/text.git"
    submodules = True

    maintainers("adamjstewart")

    version("main", branch="main")
    version("0.16.1", tag="v0.16.1", commit="66671007c84e07386da3c04e5ca403b8a417c8e5")
    version("0.16.0", tag="v0.16.0", commit="4e255c95c76b1ccde4f6650391c0bc30650d6dbe")
    version("0.15.2", tag="v0.15.2", commit="4571036cf66c539e50625218aeb99a288d79f3e1")
    version("0.15.1", tag="v0.15.1", commit="c696895e524c61fd2b8b26916dd006411c5f3ba5")
    version("0.14.1", tag="v0.14.1", commit="e1e969d4947bb3dd01ea927af2f8ac9a2d778c39")
    version("0.14.0", tag="v0.14.0", commit="e2b27f9b06ca71d55c2fcf6d47c60866ee936f40")
    version("0.13.1", tag="v0.13.1", commit="330201f1132dcd0981180c19bc6843a19d310ff0")
    version("0.13.0", tag="v0.13.0", commit="35298c43f3ce908fe06c177ecbd8ef1503a1292b")
    version("0.12.0", tag="v0.12.0", commit="d7a34d6ae0f4e36a52777854d0163b9e85f1576b")
    version("0.11.2", tag="v0.11.2", commit="92f4d158d8cbe9136896befa2d4234ea8b8e2795")
    version("0.11.1", tag="v0.11.1", commit="5c65ec05d7c1eba5b0ea2d7ee170ccf977d9674f")
    version("0.10.1", tag="v0.10.1", commit="0d670e03c1eee7e30e032bb96df4c12b785a15ff")
    version("0.10.0", tag="v0.10.0", commit="4da1de36247aa06622088e78508e0e38a4392e38")
    version("0.9.2", tag="v0.9.2", commit="22e5ee7548a85190eee78e8ed6c8911ec2c53035")
    version("0.8.1", tag="v0.8.1", commit="0f911ec35ab020983efbf36b8c14415651e98618")
    version("0.6.0", tag="0.6.0", commit="3a54c7f52584f201c17ca7489b52b812152612dc")
    version("0.5.0", tag="0.5.0", commit="0169cde2f1d446ae886ef0be07e9a673585ed256")

    # https://github.com/pytorch/text#installation
    depends_on("python@3.8:3.11", when="@0.15:", type=("build", "link", "run"))
    depends_on("python@:3.10", when="@0.13:0.14", type=("build", "link", "run"))
    depends_on("python@:3.9", when="@0.8.1:0.12", type=("build", "link", "run"))
    depends_on("python@:3.8", when="@:0.8.0", type=("build", "link", "run"))

    # CMakelists.txt
    depends_on("cmake@3.18:", when="@0.13:", type="build")
    depends_on("ninja", when="@0.13:", type="build")

    # setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-torchdata@0.7.0", when="@0.16.0", type=("build", "run"))
    depends_on("py-torchdata@0.6.1", when="@0.15.2", type=("build", "run"))
    depends_on("py-torchdata@0.6.0", when="@0.15.1", type=("build", "run"))
    depends_on("py-pybind11", when="@0.8:", type=("build", "link"))
    depends_on("py-six", when="@:0.6", type=("build", "run"))
    depends_on("py-sentencepiece", when="@:0.7", type=("build", "run"))

    # https://github.com/pytorch/text#installation
    depends_on("py-torch@main", when="@main", type=("build", "link", "run"))
    depends_on("py-torch@2.1.1", when="@0.16.1", type=("build", "link", "run"))
    depends_on("py-torch@2.1.0", when="@0.16.0", type=("build", "link", "run"))
    depends_on("py-torch@2.0.1", when="@0.15.2", type=("build", "link", "run"))
    depends_on("py-torch@2.0.0", when="@0.15.1", type=("build", "link", "run"))
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
