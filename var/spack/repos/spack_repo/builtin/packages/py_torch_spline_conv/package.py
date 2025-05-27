# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTorchSplineConv(PythonPackage):
    """Implementation of the Spline-Based Convolution Operator of SplineCNN in PyTorch."""

    homepage = "https://github.com/rusty1s/pytorch_spline_conv"
    pypi = "torch-spline-conv/torch_spline_conv-1.2.2.tar.gz"
    git = "https://github.com/rusty1s/pytorch_spline_conv.git"

    license("MIT")
    maintainers("adamjstewart")

    version("1.2.2", sha256="ed45a81da29f774665dbdd4709d7e534cdf16d2e7006dbd06957f35bd09661b2")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("python", type=("build", "link", "run"))
    # https://setuptools.pypa.io/en/latest/history.html#v77-0-0
    depends_on("py-setuptools@:76", type="build", when="@:1.2.2")
    depends_on("py-setuptools", type="build")

    # Undocumented dependencies
    depends_on("py-torch", type=("build", "link", "run"))

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if "+cuda" in self.spec["py-torch"]:
            env.set("FORCE_CUDA", "1")
            env.set("FORCE_ONLY_CUDA", "0")
            env.set("FORCE_ONLY_CPU", "0")
        else:
            env.set("FORCE_CUDA", "0")
            env.set("FORCE_ONLY_CUDA", "0")
            env.set("FORCE_ONLY_CPU", "1")
