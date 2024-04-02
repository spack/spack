# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTransformers(PythonPackage):
    """State-of-the-art Natural Language Processing for TensorFlow 2.0 and
    PyTorch"""

    homepage = "https://github.com/huggingface/transformers"
    pypi = "transformers/transformers-2.8.0.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "4.35.2",
        sha256="9dfa76f8692379544ead84d98f537be01cd1070de75c74efb13abcbc938fbe2f",
        url="https://pypi.org/packages/12/dd/f17b11a93a9ca27728e12512d167eb1281c151c4c6881d3ab59eb58f4127/transformers-4.35.2-py3-none-any.whl",
    )
    version(
        "4.31.0",
        sha256="8487aab0195ce1c2a5ae189305118b9720daddbc7b688edb09ccd79e3b149f6b",
        url="https://pypi.org/packages/21/02/ae8e595f45b6c8edee07913892b3b41f5f5f273962ad98851dc6a564bbb9/transformers-4.31.0-py3-none-any.whl",
    )
    version(
        "4.24.0",
        sha256="b7ab50039ef9bf817eff14ab974f306fd20a72350bdc9df3a858fd009419322e",
        url="https://pypi.org/packages/a4/df/3248eac2923ceffdf55686ff318e002b558e7c51f6a909dd870cf3185949/transformers-4.24.0-py3-none-any.whl",
    )
    version(
        "4.6.1",
        sha256="9d6569e31e5a4b7ab399eaf224f46ddcbb957e18a7c58cc7d469cb70e96467ea",
        url="https://pypi.org/packages/d5/43/cfe4ee779bbd6a678ac6a97c5a5cdeb03c35f9eaebbb9720b036680f9a2d/transformers-4.6.1-py3-none-any.whl",
    )
    version(
        "2.8.0",
        sha256="2b64cfe0033a47ba664837758cd9750196666ea1306e5c40ad5617353c3dc2fc",
        url="https://pypi.org/packages/a3/78/92cedda05552398352ed9784908b834ee32a0bd071a9b32de287327370b7/transformers-2.8.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@4.31:")
        depends_on("python@3.7:", when="@4.19:4.30")
        depends_on("py-boto3", when="@:2.8")
        depends_on("py-dataclasses", when="@2.7:4.18 ^python@:3.6")
        depends_on("py-filelock", when="@2.4:")
        depends_on("py-huggingface-hub@0.16.4:", when="@4.34:4.35")
        depends_on("py-huggingface-hub@0.14.1:", when="@4.29.1:4.31")
        depends_on("py-huggingface-hub@0.10.0:", when="@4.23:4.25")
        depends_on("py-huggingface-hub@0.0.8", when="@4.6:4.7")
        depends_on("py-importlib-metadata", when="@4.2:4.30 ^python@:3.7")
        depends_on("py-numpy@1.17.0:", when="@4.3:")
        depends_on("py-numpy", when="@:4.2")
        depends_on("py-packaging@20:", when="@4.11:")
        depends_on("py-packaging", when="@2.11:4.10")
        depends_on("py-pyyaml@5.1:", when="@4.9:")
        depends_on("py-regex@:2019.12.9,2019.12.18:", when="@2.3:")
        depends_on("py-requests")
        depends_on("py-sacremoses", when="@:4.18")
        depends_on("py-safetensors@0.3.1:", when="@4.30:4.37.1")
        depends_on("py-sentencepiece", when="@:3.0.0")
        depends_on("py-tokenizers@0.14.0:", when="@4.35.2:")
        depends_on("py-tokenizers@0.11.1:0.11.2,0.11.4:0.13", when="@4.23:4.33")
        depends_on("py-tokenizers@0.10.1:0.10", when="@4.3.0:4.15")
        depends_on("py-tokenizers@0.5.2:0.5", when="@2.5.1:2.8")
        depends_on("py-tqdm@4.27:", when="@2.4:")

    # Historical requirements
