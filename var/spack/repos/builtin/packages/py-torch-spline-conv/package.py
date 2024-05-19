# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchSplineConv(PythonPackage):
    """Implementation of the Spline-Based Convolution Operator of SplineCNN in PyTorch."""

    homepage = "https://github.com/rusty1s/pytorch_spline_conv"
    pypi = "torch-spline-conv/torch_spline_conv-1.2.2.tar.gz"
    git = "https://github.com/rusty1s/pytorch_spline_conv.git"

    license("MIT")
    maintainers("adamjstewart")

    version("1.2.2", sha256="ed45a81da29f774665dbdd4709d7e534cdf16d2e7006dbd06957f35bd09661b2")
    version(
        "1.2.0",
        sha256="b7a1788004f6c6143d47040f2dd7d8a579a0c69a0cb0b5d7537416bf37c082a5",
        deprecated=True,
    )

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")

    # Undocumented dependencies
    depends_on("py-torch", type=("build", "link", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", type="build", when="@:1.2.1")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@1.2.1:"):
            if "+cuda" in self.spec["py-torch"]:
                env.set("FORCE_CUDA", 1)
                env.set("FORCE_ONLY_CUDA", 0)
                env.set("FORCE_ONLY_CPU", 0)
            else:
                env.set("FORCE_CUDA", 0)
                env.set("FORCE_ONLY_CUDA", 0)
                env.set("FORCE_ONLY_CPU", 1)
        else:
            if "+cuda" in self.spec["py-torch"]:
                env.set("FORCE_CUDA", 1)
                env.set("FORCE_CPU", 0)
            else:
                env.set("FORCE_CUDA", 0)
                env.set("FORCE_CPU", 1)
