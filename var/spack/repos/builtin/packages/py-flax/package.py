# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlax(PythonPackage):
    """Flax: A neural network library for JAX designed for flexibility."""

    homepage = "https://github.com/google/flax"
    pypi = "flax/flax-0.8.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.8.1",
        sha256="8cf9ef11859eef252470377556a8cc48db287fc6647407ab34f1fc01461925dd",
        url="https://pypi.org/packages/8d/4a/7e78abc8392ff21b0257deb79e842f80647b63b745447df94893732d60fd/flax-0.8.1-py3-none-any.whl",
    )
    version(
        "0.7.3",
        sha256="abf0cf4e7dd808ae6a14e3d9f907c5eb417bf0a840f97b3ebf533fc1af60fc21",
        url="https://pypi.org/packages/32/b7/ac5df3a697fedf846f5d8f322bc998e087989ece1783bae9d26fe78c97e5/flax-0.7.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@0.7.4:")
        depends_on("py-jax@0.4.19:", when="@0.7.5:")
        depends_on("py-jax@0.4.2:", when="@:0.7.4")
        depends_on("py-msgpack")
        depends_on("py-numpy@1.23.2:", when="@0.7.5: ^python@3.11:")
        depends_on("py-numpy@1.26.0:", when="@0.7.5: ^python@3.12:")
        depends_on("py-numpy@1.22.0:", when="@0.7.5:")
        depends_on("py-numpy@1.12.0:", when="@:0.7.4")
        depends_on("py-optax")
        depends_on("py-orbax-checkpoint", when="@0.6.9:")
        depends_on("py-pyyaml@5.4.1:")
        depends_on("py-rich@11.1:")
        depends_on("py-tensorstore")
        depends_on("py-typing-extensions@4.2:", when="@0.7.3:")
