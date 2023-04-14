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

    version("2.0.1", sha256="abf4f9e10b0d97348336038db79f4efc75daa2f3f81876822273023294d6ef3e")
    version("2.0.0", sha256="dfe158aa91ac139d8bdfccc7cdb627072e0052076ae9c0459c8fa12a028dbe6c")
    version("1.9.5", sha256="4a6ee1bf338f7677f04d339b84dd0c9c0fa407c3dacea366a111dc86476d4dec")

    variant(
        "extra", default=False, description="Install extra dependencies for full functionality"
    )

    # src/lightning/__setup__.py
    depends_on("python@3.8:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # src/lightning.egg-info/requires.txt
    depends_on("py-jinja2@:4", type=("build", "run"))
    depends_on("py-pyyaml@5.4:7", type=("build", "run"))
    depends_on("py-arrow@1.2:2", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.8:5", type=("build", "run"))
    depends_on("py-click@:9", type=("build", "run"))
    depends_on("py-croniter@1.3", type=("build", "run"))
    depends_on("py-dateutils@:1", type=("build", "run"))
    depends_on("py-deepdiff@5.7:7", type=("build", "run"))
    depends_on("py-fastapi@:0.88", type=("build", "run"))
    depends_on("py-fsspec@2022.5:2023+http", type=("build", "run"))
    depends_on("py-inquirer@2.10:4", type=("build", "run"))
    depends_on("py-lightning-cloud@0.5.31:", when="@2:", type=("build", "run"))
    depends_on("py-lightning-cloud@0.5.27:", when="@:1", type=("build", "run"))
    depends_on("py-lightning-utilities@0.7:1", when="@2:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.6.0.post0:1", when="@:1", type=("build", "run"))
    depends_on("py-numpy@1.17.2:2", type=("build", "run"))
    depends_on("py-packaging@17.1:24", type=("build", "run"))
    depends_on("py-psutil@:6", type=("build", "run"))
    depends_on("py-pydantic@:2", type=("build", "run"))
    depends_on("py-requests@:3", type=("build", "run"))
    depends_on("py-rich@12.3:14", when="@2:", type=("build", "run"))
    depends_on("py-rich@:14", when="@:1", type=("build", "run"))
    depends_on("py-starlette@:1", type=("build", "run"))
    depends_on("py-starsessions@1.2.1:1", type=("build", "run"))
    depends_on("py-torch@1.11:3", when="@2:", type=("build", "run"))
    depends_on("py-torch@1.10:3", when="@:1", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:1", type=("build", "run"))
    depends_on("py-tqdm@4.57:5", type=("build", "run"))
    depends_on("py-traitlets@5.3:6", type=("build", "run"))
    depends_on("py-typing-extensions@4:5", type=("build", "run"))
    depends_on("py-urllib3@:2", type=("build", "run"))
    depends_on("py-uvicorn@:1", type=("build", "run"))
    depends_on("py-websocket-client@:2", type=("build", "run"))
    depends_on("py-websockets@:11", type=("build", "run"))
    depends_on("py-pytorch-lightning", when="@2:", type=("build", "run"))

    with when("+extra"):
        depends_on("py-aiohttp@3.8:3", type=("build", "run"))
        depends_on("py-docker@5:6", type=("build", "run"))
        depends_on("py-hydra-core@1.0.5:1", type=("build", "run"))
        depends_on("py-jsonargparse@4.18:4", when="@2:", type=("build", "run"))
        depends_on("py-jsonargparse@4.18:4+signatures", when="@:1", type=("build", "run"))
        depends_on("py-lightning-fabric@1.9:", when="@2:", type=("build", "run"))
        depends_on("py-lightning-api-access@0.0.3:", type=("build", "run"))
        depends_on("py-matplotlib@3.2:3", type=("build", "run"))
        depends_on("py-omegaconf@2.0.5:2", type=("build", "run"))
        depends_on("py-panel@0.12.7:0", type=("build", "run"))
        depends_on("py-pytorch-lightning@1.9:", when="@2:", type=("build", "run"))
        depends_on("py-pytorch-lightning@1.8.1:", when="@:1", type=("build", "run"))
        depends_on("py-redis@4.0.1:4", type=("build", "run"))
        depends_on("py-rich@12.3:13", when="@2:", type=("build", "run"))
        depends_on("py-rich@10.14:13", when="@:1", type=("build", "run"))
        depends_on("py-s3fs@2022.5:2022", type=("build", "run"))
        depends_on("py-streamlit@1.13:1", type=("build", "run"))
        depends_on("py-tensorboardx@2.2:2", type=("build", "run"))
