# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJoeynmt(PythonPackage):
    """Minimalist NMT for educational purposes"""

    homepage = "https://https://github.com/joeynmt/joeynmt"
    git = "https://github.com/joeynmt/joeynmt.git"

    version("2.2", tag="v2.2")
    version("1.5", tag="1.5")
    version("1.3", tag="1.3")

    depends_on("py-setuptools@41.0.0:", type="build")
    depends_on("python@3.5:3.9", type=("build", "run"))
    depends_on("python@3.8:", when="@1.5", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-numpy@1.20.1", when="@1.3", type=("build", "run"))
    depends_on("py-numpy@1.19.5:", when="@1.5:", type=("build", "run"))
    depends_on("py-torch@1.8.0:", when="@1.3", type=("build", "run"))
    depends_on("py-torch@1.9.0:", when="@1.5", type=("build", "run"))
    depends_on("py-torch@1.12.0:", when="@2.2", type=("build", "run"))
    depends_on("py-tensorboard@1.15:", type=("build", "run"))
    depends_on("py-torchtext@0.9.0:", when="@1.3", type=("build", "run"))
    depends_on("py-torchtext@0.10.0:0.14.0", when="@1.5", type=("build", "run"))
    depends_on("py-sacrebleu@1.3.6:", when="@1.3", type=("build", "run"))
    depends_on("py-sacrebleu@2.0.0:", when="@1.5:", type=("build", "run"))
    depends_on("py-subword-nmt", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("py-pylint", when="@1.3", type=("build", "run"))
    depends_on("py-pylint", when="@2.2", type=("build", "run"))
    depends_on("py-pylint@2.9.6:", when="@1.5", type=("build", "run"))
    depends_on("py-six@1.12.0", when="@1.3", type=("build", "run"))
    depends_on("py-six@1.12.0:", when="@1.5", type=("build", "run"))
    depends_on("py-wrapt@1.11.1", when="@:2.1", type=("build", "run"))
    depends_on("py-protobuf@3.19.4:3.20", when="@2.2", type=("build", "run"))
    depends_on("py-yapf", when="@2.2", type=("build", "run"))
    depends_on("py-flake8", when="@2.2", type=("build", "run"))
    depends_on("py-pytest", when="@2.2", type=("build", "run"))
    depends_on("py-datasets", when="@2.2", type=("build", "run"))
    depends_on("py-packaging", when="@2.2", type=("build", "run"))
    depends_on("sentencepiece", when="2.2", type=("build", "run"))
