# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAccelerate(PythonPackage):
    """A simple way to train and use PyTorch models with multi-GPU, TPU, mixed-precision."""

    homepage = "https://github.com/huggingface/accelerate"
    pypi = "accelerate/accelerate-0.16.0.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version(
        "0.21.0",
        sha256="e2609d37f2c6a56e36a0612feae6ff6d9daac9759f4899432b86b1dc97024ebb",
        url="https://pypi.org/packages/70/f9/c381bcdd0c3829d723aa14eec8e75c6c377b4ca61ec68b8093d9f35fc7a7/accelerate-0.21.0-py3-none-any.whl",
    )
    version(
        "0.16.0",
        sha256="27aa39b2076560b3ee674b9650c237c58520b3fd7907e5da1f922cf6868c1576",
        url="https://pypi.org/packages/dc/0c/f95215bc5f65e0a5fb97d4febce7c18420002a4c3ea5182294dc576f17fb/accelerate-0.16.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.21:")
        depends_on("python@3.7:", when="@0.10:0.20")
        depends_on("py-numpy@1.17.0:")
        depends_on("py-packaging@20:", when="@0.10:")
        depends_on("py-psutil", when="@0.10:")
        depends_on("py-pyyaml")
        depends_on("py-torch@1.10:", when="@0.21:")
        depends_on("py-torch@1.4:", when="@:0.18")
