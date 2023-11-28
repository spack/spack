# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchCluster(PythonPackage):
    """This package consists of a small extension library of highly optimized graph cluster
    algorithms for the use in PyTorch.
    """

    homepage = "https://github.com/rusty1s/pytorch_cluster"
    url = "https://github.com/rusty1s/pytorch_cluster/archive/1.5.7.tar.gz"

    version("1.6.3", sha256="0e2b08095e03cf87ce9b23b7a7352236a25d3ed92d92351dc020fd927ea8dbfe")
    version("1.5.8", sha256="95c6e81e9c4a6235e1b2152ab917021d2060ad995199f6bd7fb39986d37310f0")
    version("1.5.7", sha256="71701d2f7f3e458ebe5904c982951349fdb60e6f1654e19c7e102a226e2de72e")

    variant("cuda", default=False, description="Enables CUDA support")

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-torch+cuda", when="+cuda", type=("build", "link", "run"))
    depends_on("py-torch~cuda", when="~cuda", type=("build", "link", "run"))

    # https://github.com/rusty1s/pytorch_cluster/issues/120
    depends_on("py-torch~openmp", when="@:1.5 %apple-clang", type=("build", "link", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", when="@:1.5", type="build")

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            cuda_arches = list(self.spec["py-torch"].variants["cuda_arch"].value)
            for i, x in enumerate(cuda_arches):
                cuda_arches[i] = "{0}.{1}".format(x[0:-1], x[-1])
            env.set("TORCH_CUDA_ARCH_LIST", str.join(" ", cuda_arches))

            env.set("FORCE_CUDA", "1")
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
        else:
            env.set("FORCE_CUDA", "0")
