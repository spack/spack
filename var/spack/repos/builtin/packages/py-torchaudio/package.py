# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchaudio(PythonPackage):
    """The aim of torchaudio is to apply PyTorch to the audio
    domain. By supporting PyTorch, torchaudio follows the same
    philosophy of providing strong GPU acceleration, having a focus on
    trainable features through the autograd system, and having
    consistent style (tensor names and dimension names). Therefore, it
    is primarily a machine learning library and not a general signal
    processing library. The benefits of Pytorch is be seen in
    torchaudio through having all the computations be through Pytorch
    operations which makes it easy to use and feel like a natural
    extension."""

    homepage = "https://github.com/pytorch/audio"
    git = "https://github.com/pytorch/audio.git"

    version("main", branch="main", submodules=True)
    version("0.13.1", tag="v0.13.1", submodules=True)
    version("0.13.0", tag="v0.13.0", submodules=True)
    version("0.12.1", tag="v0.12.1", submodules=True)
    version("0.12.0", tag="v0.12.0", submodules=True)
    version("0.11.0", tag="v0.11.0", submodules=True)
    version("0.10.2", tag="v0.10.2", submodules=True)
    version("0.10.1", tag="v0.10.1", submodules=True)
    version("0.10.0", tag="v0.10.0", submodules=True)
    version("0.9.1", tag="v0.9.1", submodules=True)
    version("0.9.0", tag="v0.9.0", submodules=True)
    version("0.8.2", tag="v0.8.2", submodules=True)
    version("0.8.1", tag="v0.8.1", submodules=True)
    version("0.8.0", tag="v0.8.0", submodules=True)
    version("0.7.2", tag="v0.7.2", submodules=True)
    version("0.7.0", tag="v0.7.0", submodules=True)
    version("0.6.0", tag="v0.6.0", submodules=True)
    version("0.5.1", tag="v0.5.1", submodules=True)
    version("0.5.0", tag="v0.5.0", submodules=True)
    version("0.4.0", tag="v0.4.0", submodules=True)

    # https://github.com/pytorch/audio#dependencies
    depends_on("python@3.7:3.10", when="@0.12:", type=("build", "link", "run"))
    depends_on("python@3.7:3.9", when="@0.11", type=("build", "link", "run"))
    depends_on("python@3.6:3.9", when="@0.7.2:0.10", type=("build", "link", "run"))
    depends_on("python@3.6:3.8", when="@0.6:0.7.0", type=("build", "link", "run"))
    depends_on("python@3.5:3.8", when="@0.5", type=("build", "link", "run"))
    depends_on("python@2.7,3.5:3.8", when="@0.4", type=("build", "link", "run"))

    depends_on("cmake@3.18:", when="@0.10:", type="build")
    depends_on("cmake@3.5:", when="@0.8:", type="build")
    depends_on("ninja", when="@0.8:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", when="@0.12:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("sox")

    # https://github.com/pytorch/audio#dependencies
    depends_on("py-torch@master", when="@main", type=("build", "link", "run"))
    depends_on("py-torch@1.13.1", when="@0.13.1", type=("build", "link", "run"))
    depends_on("py-torch@1.13.0", when="@0.13.0", type=("build", "link", "run"))
    depends_on("py-torch@1.12.1", when="@0.12.1", type=("build", "link", "run"))
    depends_on("py-torch@1.12.0", when="@0.12.0", type=("build", "link", "run"))
    depends_on("py-torch@1.11.0", when="@0.11.0", type=("build", "link", "run"))
    depends_on("py-torch@1.10.2", when="@0.10.2", type=("build", "link", "run"))
    depends_on("py-torch@1.10.1", when="@0.10.1", type=("build", "link", "run"))
    depends_on("py-torch@1.10.0", when="@0.10.0", type=("build", "link", "run"))
    depends_on("py-torch@1.9.1", when="@0.9.1", type=("build", "link", "run"))
    depends_on("py-torch@1.9.0", when="@0.9.0", type=("build", "link", "run"))
    depends_on("py-torch@1.8.2", when="@0.8.2", type=("build", "link", "run"))
    depends_on("py-torch@1.8.1", when="@0.8.1", type=("build", "link", "run"))
    depends_on("py-torch@1.8.0", when="@0.8.0", type=("build", "link", "run"))
    depends_on("py-torch@1.7.1", when="@0.7.2", type=("build", "link", "run"))
    depends_on("py-torch@1.7.0", when="@0.7.0", type=("build", "link", "run"))
    depends_on("py-torch@1.6.0", when="@0.6.0", type=("build", "link", "run"))
    depends_on("py-torch@1.5.1", when="@0.5.1", type=("build", "link", "run"))
    depends_on("py-torch@1.5.0", when="@0.5.0", type=("build", "link", "run"))
    depends_on("py-torch@1.4.1", when="@0.4.0", type=("build", "link", "run"))

    def setup_build_environment(self, env):
        # tools/setup_helpers/extension.py
        env.set("BUILD_SOX", 0)

        if "+cuda" in self.spec["py-torch"]:
            env.set("USE_CUDA", 1)
            torch_cuda_arch_list = ";".join(
                "{0:.1f}".format(float(i) / 10.0)
                for i in self.spec["py-torch"].variants["cuda_arch"].value
            )
            env.set("TORCH_CUDA_ARCH_LIST", torch_cuda_arch_list)
        else:
            env.set("USE_CUDA", 0)

        if "+rocm" in self.spec["py-torch"]:
            env.set("USE_ROCM", 1)
        else:
            env.set("USE_ROCM", 0)
