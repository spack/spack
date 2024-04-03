# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVectorQuantizePytorch(PythonPackage):
    """A vector quantization library originally transcribed
    from Deepmind's tensorflow implementation, made
    conveniently into a package. It uses exponential moving
    averages to update the dictionary."""

    homepage = "https://github.com/lucidrains/vector-quantize-pytorch"
    pypi = "vector_quantize_pytorch/vector_quantize_pytorch-0.3.9.tar.gz"

    license("MIT")

    version(
        "0.3.9",
        sha256="524f5a8cdad54b039ebc86320bef3dc2da633100af34e70bea1ddf09458bcfa2",
        url="https://pypi.org/packages/f4/e3/4fddac6653e017ce643448beb8a2af4a437ecd58aa663f859d065b2a8e00/vector_quantize_pytorch-0.3.9-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-einops", when="@0.3:1.0.2")
        depends_on("py-torch")
