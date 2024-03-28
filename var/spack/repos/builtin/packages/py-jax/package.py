# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJax(PythonPackage):
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

    license("Apache-2.0")

    version("0.4.25", sha256="a8ee189c782de2b7b2ffb64a8916da380b882a617e2769aa429b71d79747b982")
    version("0.4.23", sha256="2a229a5a758d1b803891b2eaed329723f6b15b4258b14dc0ccb1498c84963685")
    version("0.4.16", sha256="e2ca82c9bf973c2c1c01f5340a583692b31f277aa3abd0544229c1fe5fa44b02")
    version("0.4.3", sha256="d43f08f940aa30eb339965cfb3d6bee2296537b0dc2f0c65ccae3009279529ae")
    version(
        "0.3.23",
        sha256="bff436e15552a82c0ebdef32737043b799e1e10124423c57a6ae6118c3a7b6cd",
        deprecated=True,
    )
    version(
        "0.2.25",
        sha256="822e8d1e06257eaa0fdc4c0a0686c4556e9f33647fa2a766755f984786ae7446",
        deprecated=True,
    )

    depends_on("python@3.9:", when="@0.4.14:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-ml-dtypes@0.2:", when="@0.4.14:", type=("build", "run"))
    depends_on("py-ml-dtypes@0.1:", when="@0.4.9:", type=("build", "run"))
    depends_on("py-ml-dtypes@0.0.3:", when="@0.4.7:", type=("build", "run"))
    depends_on("py-numpy@1.22:", when="@0.4.14:", type=("build", "run"))
    depends_on("py-numpy@1.21:", when="@0.4.7:", type=("build", "run"))
    depends_on("py-numpy@1.20:", when="@0.3:", type=("build", "run"))
    depends_on("py-numpy@1.18:", type=("build", "run"))
    depends_on("py-opt-einsum", type=("build", "run"))
    depends_on("py-scipy@1.9:", when="@0.4.19:", type=("build", "run"))
    depends_on("py-scipy@1.7:", when="@0.4.7:", type=("build", "run"))
    depends_on("py-scipy@1.5:", when="@0.3:", type=("build", "run"))
    depends_on("py-scipy@1.2.1:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.6:", when="@0.4.11: ^python@:3.9", type=("build", "run"))

    # See jax/_src/lib/__init__.py
    # https://github.com/google/jax/commit/8be057de1f50756fe7522f7e98b2f30fad56f7e4
    for v in ["0.4.25", "0.4.23", "0.4.16", "0.4.3", "0.3.23"]:
        depends_on(f"py-jaxlib@:{v}", when=f"@{v}", type=("build", "run"))

    # See _minimum_jaxlib_version in jax/version.py
    depends_on("py-jaxlib@0.4.20:", when="@0.4.25:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.19:", when="@0.4.21:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.14:", when="@0.4.15:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.11:", when="@0.4.12:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.7:", when="@0.4.8:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.6:", when="@0.4.7:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.4:", when="@0.4.5:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.2:", when="@0.4.3:", type=("build", "run"))
    depends_on("py-jaxlib@0.4.1:", when="@0.4.2:", type=("build", "run"))
    depends_on("py-jaxlib@0.3.22:", when="@0.3.24:", type=("build", "run"))
    depends_on("py-jaxlib@0.3.15:", when="@0.3.18:", type=("build", "run"))
    depends_on("py-jaxlib@0.3.14:", when="@0.3.15:", type=("build", "run"))
    depends_on("py-jaxlib@0.3.7:", when="@0.3.8:", type=("build", "run"))
    depends_on("py-jaxlib@0.3.2:", when="@0.3.7:", type=("build", "run"))
    depends_on("py-jaxlib@0.3.0:", when="@0.3.2:", type=("build", "run"))
    depends_on("py-jaxlib@0.1.74:", when="@0.2.26:", type=("build", "run"))
    depends_on("py-jaxlib@0.1.69:", when="@0.2.18:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-absl-py", when="@:0.3", type=("build", "run"))
    depends_on("py-typing-extensions", when="@:0.3", type=("build", "run"))
    depends_on("py-etils+epath", when="@0.3", type=("build", "run"))
