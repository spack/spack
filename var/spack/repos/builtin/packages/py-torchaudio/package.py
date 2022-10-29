# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    version("0.13.0", tag="v0.13.0", submodules=True)
    version("0.4.0", tag="v0.4.0", submodules=True)

    depends_on("cmake@3.18:", when="@0.10:", type="build")
    depends_on("cmake@3.5:", when="@0.8:", type="build")
    depends_on("py-setuptools", type="build")

    # https://github.com/pytorch/audio#dependencies
    depends_on("py-torch@master", when="@main", type=("build", "run"))
    depends_on("py-torch@1.13.0", when="@0.13.0", type=("build", "run"))
    depends_on("py-torch@1.4.0", when="@0.4.0", type=("build", "run"))

    def setup_build_environment(self, env):
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
