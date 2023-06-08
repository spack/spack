# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThinc(PythonPackage):
    """Thinc: Practical Machine Learning for NLP in Python."""

    homepage = "https://github.com/explosion/thinc"
    pypi = "thinc/thinc-7.4.1.tar.gz"

    version("8.1.10", sha256="6c4a48d7da07e044e84a68cbb9b22f32f8490995a2bab0bfc60e412d14afb991")
    version("7.4.1", sha256="0139fa84dc9b8d88af15e648fc4ae13d899b8b5e49cb26a8f4a0604ee9ad8a9e")
    version("7.4.0", sha256="523e9be1bfaa3ed1d03d406ce451b6b4793a9719d5b83d2ea6b3398b96bc58b8")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.25:2", type="build")

    depends_on("py-murmurhash@0.28:1.0", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-murmurhash@1.0.2:1.0", type=("build", "run"), when="@8.1.10:")

    depends_on("py-cymem@2.0.2:2.0", type=("build", "run"))

    depends_on("py-preshed@1.0.1:3.0", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-preshed@3.0.2:3.0", type=("build", "run"), when="@8.1.10:")

    depends_on("py-blis@0.4.0:0.4", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-blis@0.7.8:0.7", type=("build", "run"), when="@8.1.10:")

    depends_on("py-wasabi@0.0.9:1.0", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-wasabi@0.8.1:1.1", type=("build", "run"), when="@8.1.10:")

    depends_on("py-srsly@0.0.6:1.0", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-srsly@2.4:2", type=("build", "run"), when="@8.1.10:")

    depends_on("py-catalogue@0.0.7:1.0", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-catalogue@2.0.4:2.0", type=("build", "run"), when="@8.1.10:")

    depends_on("py-confection@0.0.1:0", type=("build", "run"), when="@8.1.10:")

    depends_on("py-numpy@1.7:", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-numpy@1.15:", type=("build", "run"), when="@8.1.10:")

    depends_on("py-pydantic@1.7.4:1.7,1.9:1.10", type=("build", "run"), when="@8.1.10:")
    depends_on("py-packaging@20:", type=("build", "run"), when="@8.1.10:")

    depends_on("py-dataclasses@0.6:0", type=("build", "run"), when="@8.1.10:^python@:3.6")
    depends_on("py-typing-extensions@3.7.4.1:4.4", type=("build", "run"), when="@8.1.10:^3.7")
    depends_on("py-contextvars@2.4:2", type=("build", "run"), when="@8.1.10:^3.6")

    depends_on("py-plac@0.9.6:1.1", type=("build", "run"), when="@7.4.0:7.4.1")
    depends_on("py-tqdm@4.10:4", type=("build", "run"), when="@7.4.0:7.4.1")
