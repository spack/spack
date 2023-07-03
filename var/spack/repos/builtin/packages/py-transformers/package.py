# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    version("4.24.0", sha256="486f353a8e594002e48be0e2aba723d96eda839e63bfe274702a4b5eda85559b")
    version("4.6.1", sha256="83dbff763b7e7dc57cbef1a6b849655d4fcab6bffdd955c5e8bea12a4f76dc10")
    version("2.8.0", sha256="b9f29cdfd39c28f29e0806c321270dea337d6174a7aa60daf9625bf83dbb12ee")

    depends_on("python@3.7:", when="@4.24:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-importlib-metadata", when="@4.6: ^python@:3.7", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-huggingface-hub@0.10:0", when="@4.24:", type=("build", "run"))
    depends_on("py-huggingface-hub@0.0.8", when="@4.6.1", type=("build", "run"))
    depends_on("py-numpy@1.17:", when="@4.6:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging@20:", when="@4.24:", type=("build", "run"))
    depends_on("py-packaging", when="@4.6.1", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", when="@4.24:", type=("build", "run"))
    depends_on("py-regex@:2019.12.16,2019.12.18:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-tokenizers@0.11.1:0.11.2,0.11.4:0.13", when="@4.24:", type=("build", "run"))
    depends_on("py-tokenizers@0.10.1:0.10", when="@4.6.1", type=("build", "run"))
    depends_on("py-tokenizers@0.5.2", when="@2.8.0", type=("build", "run"))
    depends_on("py-tqdm@4.27:", type=("build", "run"))

    # Historical requirements
    depends_on("py-sacremoses", when="@:4.6", type=("build", "run"))
    depends_on("py-boto3", when="@2.8.0", type=("build", "run"))
    depends_on("py-sentencepiece", when="@2.8.0", type=("build", "run"))
