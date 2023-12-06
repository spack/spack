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

    version("4.35.2", sha256="2d125e197d77b0cdb6c9201df9fa7e2101493272e448b9fba9341c695bee2f52")
    version("4.31.0", sha256="4302fba920a1c24d3a429a29efff6a63eac03f3f3cf55b55927fc795d01cb273")
    version("4.24.0", sha256="486f353a8e594002e48be0e2aba723d96eda839e63bfe274702a4b5eda85559b")
    version("4.6.1", sha256="83dbff763b7e7dc57cbef1a6b849655d4fcab6bffdd955c5e8bea12a4f76dc10")
    version("2.8.0", sha256="b9f29cdfd39c28f29e0806c321270dea337d6174a7aa60daf9625bf83dbb12ee")

    depends_on("py-setuptools", type="build")
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-huggingface-hub@0.16.4:0", when="@4.34:", type=("build", "run"))
    depends_on("py-huggingface-hub@0.14.1:0", when="@4.26:", type=("build", "run"))
    depends_on("py-huggingface-hub@0.10:0", when="@4.24:", type=("build", "run"))
    depends_on("py-huggingface-hub@0.0.8", when="@4.6.1", type=("build", "run"))
    depends_on("py-numpy@1.17:", when="@4.6:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging@20:", when="@4.24:", type=("build", "run"))
    depends_on("py-packaging", when="@4.6.1", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", when="@4.24:", type=("build", "run"))
    depends_on("py-regex@:2019.12.16,2019.12.18:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-safetensors@0.3.1:", when="@4.31:", type=("build", "run"))
    depends_on("py-tokenizers@0.14:0.18", when="@4.35:", type=("build", "run"))
    depends_on("py-tokenizers@0.11.1:0.11.2,0.11.4:0.13", when="@4.24:4.33", type=("build", "run"))
    depends_on("py-tokenizers@0.10.1:0.10", when="@4.6.1", type=("build", "run"))
    depends_on("py-tokenizers@0.5.2", when="@2.8.0", type=("build", "run"))
    depends_on("py-tqdm@4.27:", type=("build", "run"))

    # Historical requirements
    depends_on("py-sacremoses", when="@:4.6", type=("build", "run"))
    depends_on("py-boto3", when="@2.8.0", type=("build", "run"))
    depends_on("py-sentencepiece", when="@2.8.0", type=("build", "run"))
