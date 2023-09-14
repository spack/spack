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
    version(
        "2.0.2", tag="v2.0.2", commit="31de77dad5c89274451b3f5c4bcb630be12787c4", submodules=True
    )
    version(
        "2.0.1", tag="v2.0.1", commit="3b40834aca41957002dfe074175e900cf8906237", submodules=True
    )
    version(
        "0.13.1", tag="v0.13.1", commit="b90d79882c3521fb3882833320b4b85df3b622f4", submodules=True
    )
    version(
        "0.13.0", tag="v0.13.0", commit="bc8640b4722abf6587fb4cc2521da45aeb55a711", submodules=True
    )
    version(
        "0.12.1", tag="v0.12.1", commit="58da31733e08438f9d1816f55f54756e53872a92", submodules=True
    )
    version(
        "0.12.0", tag="v0.12.0", commit="2e1388401c434011e9f044b40bc8374f2ddfc414", submodules=True
    )
    version(
        "0.11.0", tag="v0.11.0", commit="820b383b3b21fc06e91631a5b1e6ea1557836216", submodules=True
    )
    version(
        "0.10.2", tag="v0.10.2", commit="6f539cf3edc4224b51798e962ca28519e5479ffb", submodules=True
    )
    version(
        "0.10.1", tag="v0.10.1", commit="4b64f80bef85bd951ea35048c461c8304e7fc4c4", submodules=True
    )
    version(
        "0.10.0", tag="v0.10.0", commit="d2634d866603c1e2fc8e44cd6e9aea7ddd21fe29", submodules=True
    )
    version(
        "0.9.1", tag="v0.9.1", commit="a85b2398722182dd87e76d9ffcbbbf7e227b83ce", submodules=True
    )
    version(
        "0.9.0", tag="v0.9.0", commit="33b2469744955e2129c6367457dffe9bb4b05dea", submodules=True
    )
    version(
        "0.8.2", tag="v0.8.2", commit="d254d547d183e7203e455de6b99e56d3ffdd4499", submodules=True
    )
    version(
        "0.8.1", tag="v0.8.1", commit="e4e171a51714b2b2bd79e1aea199c3f658eddf9a", submodules=True
    )
    version(
        "0.8.0", tag="v0.8.0", commit="099d7883c6b7af1d1c3b416191e5f3edf492e104", submodules=True
    )
    version(
        "0.7.2", tag="v0.7.2", commit="a853dff25de36cc637b1f02029343790d2dd0199", submodules=True
    )
    version(
        "0.7.0", tag="v0.7.0", commit="ac17b64f4daedd45d0495e2512e22eaa6e5b7eeb", submodules=True
    )
    version(
        "0.6.0", tag="v0.6.0", commit="f17ae39ff9da0df8f795fef2fcc192f298f81268", submodules=True
    )
    version(
        "0.5.1", tag="v0.5.1", commit="71434798460a4ceca9d42004567ef419c62a612e", submodules=True
    )
    version(
        "0.5.0", tag="v0.5.0", commit="09494ea545738538f9db2dceeffe10d421060ee5", submodules=True
    )
    version(
        "0.4.0", tag="v0.4.0", commit="8afed303af3de41f3586007079c0534543c8f663", submodules=True
    )

    # https://github.com/pytorch/audio#dependencies
    depends_on("python@3.8:3.11", when="@2:", type=("build", "link", "run"))
    depends_on("python@3.7:3.10", when="@0.12:0", type=("build", "link", "run"))
    depends_on("python@3.7:3.9", when="@0.11", type=("build", "link", "run"))
    depends_on("python@3.6:3.9", when="@0.7.2:0.10", type=("build", "link", "run"))
    depends_on("python@3.6:3.8", when="@0.6:0.7.0", type=("build", "link", "run"))
    depends_on("python@3.5:3.8", when="@0.5", type=("build", "link", "run"))
    depends_on("python@2.7,3.5:3.8", when="@0.4", type=("build", "link", "run"))

    # CMakelists.txt
    depends_on("cmake@3.18:", when="@0.10:", type="build")
    depends_on("cmake@3.5:", when="@0.8:", type="build")
    depends_on("ninja", when="@0.8:", type="build")

    # setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", when="@0.12:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("sox")

    # https://github.com/pytorch/audio#dependencies
    depends_on("py-torch@master", when="@main", type=("build", "link", "run"))
    depends_on("py-torch@2.0.1", when="@2.0.2", type=("build", "link", "run"))
    depends_on("py-torch@2.0.0", when="@2.0.1", type=("build", "link", "run"))
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
