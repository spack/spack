# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightly(PythonPackage):
    """A deep learning package for self-supervised learning."""

    homepage = "https://www.lightly.ai/"
    # https://github.com/lightly-ai/lightly/issues/1146
    url = "https://github.com/lightly-ai/lightly/archive/refs/tags/v1.4.1.tar.gz"

    maintainers("adamjstewart")

    version("1.4.2", sha256="bae451fcd04fbd3cc14b044a2583ae24591533d4a8a6ff51e5f1477f9a077648")
    version("1.4.1", sha256="4c64657639c66ee5c8b4b8d300fc9b5287dc7e14a260f3a2e04917dca7f57f5b")

    # lightly/requirements/base.txt
    depends_on("py-certifi@14.05.14:", type=("build", "run"))
    depends_on("py-hydra-core@1:", type=("build", "run"))
    depends_on("py-lightly-utils@0.0", type=("build", "run"))
    depends_on("py-numpy@1.18.1:", type=("build", "run"))
    depends_on("py-python-dateutil@2.5.3:", type=("build", "run"))
    depends_on("py-requests@2.23:", type=("build", "run"))
    depends_on("py-setuptools@21:", when="@1.4.2:", type="build")
    depends_on("py-setuptools@21:65.5.1", when="@:1.4.1", type=("build", "run"))
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("py-tqdm@4.44:", type=("build", "run"))
    depends_on("py-urllib3@1.15.1:", type=("build", "run"))

    # lightly/requirements/torch.txt
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-torch@:1", when="@:1.4.1", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-pytorch-lightning@1.0.4:", type=("build", "run"))
    depends_on("py-pytorch-lightning@1.0.4:1", when="@:1.4.1", type=("build", "run"))

    # https://github.com/lightly-ai/lightly/issues/1153
    depends_on("py-torch+distributed", type=("build", "run"))
