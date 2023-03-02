# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJax(PythonPackage, CudaPackage):
    """JAX is Autograd and XLA, brought together for high-performance
    machine learning research. With its updated version of Autograd,
    JAX can automatically differentiate native Python and NumPy
    functions. It can differentiate through loops, branches,
    recursion, and closures, and it can take derivatives of
    derivatives of derivatives. It supports reverse-mode
    differentiation (a.k.a. backpropagation) via grad as well as
    forward-mode differentiation, and the two can be composed
    arbitrarily to any order."""

    homepage = "https://github.com/google/jax"
    pypi = "jax/jax-0.2.25.tar.gz"

    version("0.2.25", sha256="822e8d1e06257eaa0fdc4c0a0686c4556e9f33647fa2a766755f984786ae7446")

    variant("cuda", default=True, description="CUDA support")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.18:", type=("build", "run"))
    depends_on("py-absl-py", type=("build", "run"))
    depends_on("py-opt-einsum", type=("build", "run"))
    depends_on("py-scipy@1.2.1:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-jaxlib@0.1.69:", type=("build", "run"), when="~cuda")
    depends_on("py-jaxlib@0.1.69:+cuda", type=("build", "run"), when="+cuda")
    for arch in CudaPackage.cuda_arch_values:
        depends_on(
            "py-jaxlib@0.1.69:+cuda cuda_arch={0}".format(arch),
            type=("build", "run"),
            when="cuda_arch={0}".format(arch),
        )
