# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchCluster(PythonPackage):
    """PyTorch Extension Library of Optimized Graph Cluster Algorithms."""

    homepage = "https://github.com/rusty1s/pytorch_cluster"
    pypi = "torch-cluster/torch_cluster-1.6.3.tar.gz"
    git = "https://github.com/rusty1s/pytorch_cluster.git"

    license("MIT")
    maintainers("adamjstewart")

    version("1.6.3", sha256="78d5a930a5bbd0d8788df8c6d66addd68d6dd292fe3edb401e3dacba26308152")
    version(
        "1.5.8",
        sha256="a0a32f63faac40a026ab1e9da31f6babdb4d937e53be40bd1c91d9b5a286eee6",
        deprecated=True,
    )
    version(
        "1.5.7",
        sha256="62a3ec1bebadda1a4a2c867203f4c957b9c0b9d11ffb03b40b8ea9f95a0a4d3b",
        deprecated=True,
    )

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))

    # Undocumented dependencies
    depends_on("py-torch", type=("build", "link", "run"))

    # https://github.com/rusty1s/pytorch_cluster/issues/120
    depends_on("py-torch~openmp", when="@:1.5 %apple-clang", type=("build", "link", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", when="@:1.5", type="build")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@1.5.9:"):
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
