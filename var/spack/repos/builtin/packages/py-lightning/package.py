# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightning(PythonPackage):
    """Use Lightning Apps to build everything from production-ready,
    multi-cloud ML systems to simple research demos.
    """

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "lightning/lightning-2.0.0.tar.gz"

    maintainers("adamjstewart")

    version("2.0.0", sha256="dfe158aa91ac139d8bdfccc7cdb627072e0052076ae9c0459c8fa12a028dbe6c")
    version("1.9.4", sha256="842d81c48ed0684d2e33b4d815794f9c3b2adb3916446ed12556dfeb3952e721")
    version("1.9.3", sha256="1d594b756d619b65ed61cf2fc17511819565ec94f70a49e797bd9b8e435d7c0c")
    version("1.9.2", sha256="056bef8c9a5f3cfa82d07a65798a524d3a90fbb9e07d155f8da3194b24151593")
    version("1.9.1", sha256="d13e4b364361ddb8d0380b41f069f13e6f8f6b10d6ed3c34ceafa7e6007d6007")
    version("1.9.0", sha256="d002270e2cd6bdf239d6605f8ec7f6f79bd2ec4eb5e7758b38ca36c57d4d1fdf")
    version("1.8.6", sha256="4f56a390e58551cf40173c8c74684972c261185f3a92690888340b7209855f49")
    version("1.8.5", sha256="c54b2369a51c613ab4324c61c56af2d6100b9431ac0d7ae31c8d646561873eb4")
    version("1.8.4", sha256="4f7746b406276449bd91b46c71eaf8823781322e56dec860316c74560e7e8551")
    version("1.8.3", sha256="61b03b7858848ac01aea3d76679104bc651271697c40f13cc078ad4365594874")
    version("1.8.2", sha256="f30e30b9eaa8a0986fbaec61734775ba349185ed17bd7f02caa2af4ff75e273e")
    version("1.8.1", sha256="c0a5dda56f62efd807ccf18a2943fbf8ca60511f8afa63ec3ab1ebe79e43575c")

    variant(
        "extra", default=False, description="Install extra dependencies for full functionality"
    )

    # src/pytorch_lightning/__setup__.py
    depends_on("python@3.8:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # requirements/pytorch/base.txt
    depends_on("py-numpy@1.17.2:", type=("build", "run"))
    depends_on("py-torch@1.11:", when="@2:", type=("build", "run"))
    depends_on("py-torch@1.10:", when="@1.9:", type=("build", "run"))
    depends_on("py-torch@1.9:", type=("build", "run"))
    depends_on("py-tqdm@4.57.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.4:", type=("build", "run"))
    depends_on("py-fsspec@2021.06.1:+http", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:", type=("build", "run"))
    depends_on("py-packaging@17.1:", when="@1.9:", type=("build", "run"))
    depends_on("py-packaging@17.0:", type=("build", "run"))
    depends_on("py-typing-extensions@4:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.7:", when="@2:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.6.0.post0:", when="@1.9.1:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.4.2:", when="@1.9.0", type=("build", "run"))
    depends_on("py-lightning-utilities@0.3,0.4.1:", when="@1.8.4:1.8", type=("build", "run"))
    depends_on("py-lightning-utilities@0.3:", when="@1.8.0:1.8.3", type=("build", "run"))

    # requirements/pytorch/extra.txt
    with when("+extra"):
        depends_on("py-matplotlib@3.2:", type=("build", "run"))
        depends_on("py-omegaconf@2.0.5:", type=("build", "run"))
        depends_on("py-hydra-core@1.0.5:", type=("build", "run"))
        depends_on("py-jsonargparse@4.18:+signatures", when="@1.9:", type=("build", "run"))
        depends_on("py-jsonargparse@4.15.2:+signatures", type=("build", "run"))
        depends_on("py-rich@12.3:", when="@2:", type=("build", "run"))
        depends_on("py-rich@10.14:", type=("build", "run"))
        depends_on("py-tensorboardx@2.2:", when="@1.9:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-lightning-lite@1.8.0", when="@1.8.0", type=("build", "run"))
    depends_on("py-tensorboardx@2.2:", when="@1.8.3:1.8", type=("build", "run"))
    depends_on("py-tensorboard@2.9.1:", when="@:1.8.2", type=("build", "run"))

    # https://github.com/Lightning-AI/lightning/issues/16637
    conflicts("^py-torch~distributed", when="@1.9.0")
    # https://github.com/Lightning-AI/lightning/issues/15494
    conflicts("^py-torch~distributed", when="@1.8.0")
