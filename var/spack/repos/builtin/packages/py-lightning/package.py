# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightning(PythonPackage):
    """The Deep Learning framework to train, deploy, and ship AI products Lightning fast."""

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "lightning/lightning-2.0.0.tar.gz"
    skip_modules = ["lightning.app", "lightning.data", "lightning.store"]

    maintainers("adamjstewart")

    version("2.1.2", sha256="3b2599a8a719916cb03526e6570356809729680c6cda09391232e2aba0a4ed4b")
    version("2.1.1", sha256="865491940d20a9754eac7494aa18cab893e0c2b31e83743349eeeaf31dfb52db")
    version("2.1.0", sha256="1f78f5995ae7dcffa1edf34320db136902b73a0d1b304404c48ec8be165b3a93")
    version("2.0.9", sha256="2395ece6e29e12064718ff16b8edec5685df7f7095d4fee78edb0a654f5cd7eb")
    version("2.0.8", sha256="db914e211b5c3b079a821be6e4344e72d0a729163676a65c4e00aae98390ae7b")
    version("2.0.7", sha256="f05acd4ba846505d40125b4f9f0bda0804b2b0356e2ad2fd4e4bf7d1c61c8cc6")
    version("2.0.6", sha256="bff959f65eed2f626dd65e7b2cfd0d3ddcd0c4ca19ffc8f5f49a4ba4494ca528")
    version("2.0.5", sha256="77df233129b29c11df7b5e071e24e29420d5efbdbbac9cb6fb4602b7b5afce8a")
    version("2.0.4", sha256="f5f5ed75a657caa8931051590ed000d46bf1b8311ae89bb17a961c3f299dbf33")
    version("2.0.3", sha256="5a70f05e40f1d7882f81eace0d4a86fe2604b423f8df42beaabd187bfdb420cf")
    version("2.0.2", sha256="fa32d671850a5be2d961c6705c927f6f48d1cf9696f61f7d865244142e684430")
    version("2.0.1", sha256="abf4f9e10b0d97348336038db79f4efc75daa2f3f81876822273023294d6ef3e")
    version("2.0.0", sha256="dfe158aa91ac139d8bdfccc7cdb627072e0052076ae9c0459c8fa12a028dbe6c")
    version("1.9.5", sha256="4a6ee1bf338f7677f04d339b84dd0c9c0fa407c3dacea366a111dc86476d4dec")

    # src/lightning/__setup__.py
    depends_on("python@3.8:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # src/lightning.egg-info/requires.txt
    depends_on("py-pyyaml@5.4:7", type=("build", "run"))
    depends_on("py-fsspec@2021.6.1:2024+http", when="@2.1:", type=("build", "run"))
    depends_on("py-fsspec@2022.5:2024+http", when="@2.0.5:2.0", type=("build", "run"))
    depends_on("py-fsspec@2022.5:2023+http", when="@:2.0.4", type=("build", "run"))
    depends_on("py-lightning-utilities@0.8:1", when="@2.1:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.7:1", when="@2.0", type=("build", "run"))
    depends_on("py-lightning-utilities@0.6.0.post0:1", when="@:1", type=("build", "run"))
    depends_on("py-numpy@1.17.2:2", type=("build", "run"))
    depends_on("py-packaging@20:24", when="@2.1:", type=("build", "run"))
    depends_on("py-packaging@17.1:24", when="@:2.0", type=("build", "run"))
    depends_on("py-torch@1.12:3", when="@2.1:", type=("build", "run"))
    depends_on("py-torch@1.11:3", when="@2.0", type=("build", "run"))
    depends_on("py-torch@1.10:3", when="@:1", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:2", when="@2.0.9:", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:1", when="@:2.0.8", type=("build", "run"))
    depends_on("py-tqdm@4.57:5", type=("build", "run"))
    depends_on("py-typing-extensions@4:5", type=("build", "run"))

    # Only an alias, not actually used by the library
    # depends_on("py-pytorch-lightning", when="@2:", type=("build", "run"))

    # Historical requirements
    with when("@:2.0"):
        depends_on("py-jinja2@:4", type=("build", "run"))
        depends_on("py-arrow@1.2:2", type=("build", "run"))
        depends_on("py-backoff@2.2.1:3", when="@2.0.5:", type=("build", "run"))
        depends_on("py-beautifulsoup4@4.8:5", type=("build", "run"))
        depends_on("py-click@:9", type=("build", "run"))
        depends_on("py-croniter@1.3:1.4", when="@2.0.5:", type=("build", "run"))
        depends_on("py-croniter@1.3", when="@:2.0.4", type=("build", "run"))
        depends_on("py-dateutils@:1", type=("build", "run"))
        depends_on("py-deepdiff@5.7:7", type=("build", "run"))
        depends_on("py-fastapi@0.92:1", when="@2.0.4:", type=("build", "run"))
        depends_on("py-fastapi@0.69:0.88", when="@2.0.3", type=("build", "run"))
        depends_on("py-fastapi@:0.88", when="@:2.0.2", type=("build", "run"))
        depends_on("py-inquirer@2.10:4", type=("build", "run"))
        depends_on("py-lightning-cloud@0.5.38:", when="@2.0.9:", type=("build", "run"))
        depends_on("py-lightning-cloud@0.5.37:", when="@2.0.5:", type=("build", "run"))
        depends_on("py-lightning-cloud@0.5.34:", when="@2.0.3:", type=("build", "run"))
        depends_on("py-lightning-cloud@0.5.31:", when="@2:", type=("build", "run"))
        depends_on("py-lightning-cloud@0.5.27:", when="@:1", type=("build", "run"))
        depends_on("py-psutil@:6", type=("build", "run"))
        depends_on("py-pydantic@1.7.4:2.1", when="@2.0.7:", type=("build", "run"))
        depends_on("py-pydantic@1.7.4:2.0", when="@2.0.6", type=("build", "run"))
        depends_on("py-pydantic@1.7.4:1", when="@2.0.5", type=("build", "run"))
        depends_on("py-pydantic@1.7.4:3", when="@2.0.3:2.0.4", type=("build", "run"))
        depends_on("py-pydantic@:2", when="@:2.0.2", type=("build", "run"))
        depends_on("py-python-multipart@0.0.5:1", type=("build", "run"))
        depends_on("py-requests@:3", type=("build", "run"))
        depends_on("py-rich@12.3:14", when="@2:", type=("build", "run"))
        depends_on("py-rich@:14", when="@:1", type=("build", "run"))
        depends_on("py-starlette", when="@2.0.3:", type=("build", "run"))
        depends_on("py-starlette@:1", when="@:2.0.2", type=("build", "run"))
        depends_on("py-starsessions@1.2.1:1", type=("build", "run"))
        depends_on("py-traitlets@5.3:6", type=("build", "run"))
        depends_on("py-urllib3@:3", when="@2.0.4:", type=("build", "run"))
        depends_on("py-urllib3@:2", when="@:2.0.3", type=("build", "run"))
        depends_on("py-uvicorn@:1", type=("build", "run"))
        depends_on("py-websocket-client@:2", type=("build", "run"))
        depends_on("py-websockets@:12", when="@2.0.5:", type=("build", "run"))
        depends_on("py-websockets@:11", when="@:2.0.4", type=("build", "run"))

    # https://github.com/Lightning-AI/lightning/issues/18858
    conflicts("^py-torch~distributed", when="@2.1.0")
