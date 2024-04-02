# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlab(PythonPackage):
    """JupyterLab is the next-generation web-based user interface
    for Project Jupyter."""

    homepage = "https://github.com/jupyterlab/jupyterlab"
    pypi = "jupyterlab/jupyterlab-2.2.7.tar.gz"

    license("BSD-3-Clause")

    version(
        "4.0.1",
        sha256="f3ebd90e41d3ba1b8152c8eda2bd1a18e0de490192b4be1a6ec132517cfe43ef",
        url="https://pypi.org/packages/77/94/0d4f2a8dc006eb4f510cb714a3fbe3b8931c45943fd95c6159509bb8edc7/jupyterlab-4.0.1-py3-none-any.whl",
    )
    version(
        "3.4.8",
        sha256="4626a0434c76a3a22f11c4efaa1d031d2586367f72cfdbdbff6b08b6ef0060f7",
        url="https://pypi.org/packages/9b/67/be3e254f846d5a143edc385bdfd61ee366be70a3223808f30f0b6b3d8f62/jupyterlab-3.4.8-py3-none-any.whl",
    )
    version(
        "3.4.2",
        sha256="f749fff221e12fe384dd91e6f8c004e6a59cd3bf4271208002ab02cb4218618c",
        url="https://pypi.org/packages/90/53/3eb1697790df866f847600b9aaa5e82e72dbeae8160b2fda7bda70bb4454/jupyterlab-3.4.2-py3-none-any.whl",
    )
    version(
        "3.2.9",
        sha256="729d1f06e97733070badc04152aecf9fb2cd036783eebbd9123ff58aab83a8f5",
        url="https://pypi.org/packages/4b/0d/03deff4501e9ffafe755e561e375ffa9f5822fec93a09ce1c7c5147bdcb3/jupyterlab-3.2.9-py3-none-any.whl",
    )
    version(
        "3.2.1",
        sha256="6fe0240f1880cde1325072b9ff1ef2f442784de4aed5df1ab802a027c9791f62",
        url="https://pypi.org/packages/b7/ed/f47b38a48d67726862e9c1237c079150154a00bbcc60c25731f8211ad850/jupyterlab-3.2.1-py3-none-any.whl",
    )
    version(
        "3.1.19",
        sha256="5fea3ceed4ad364a175b5ec85220c9b6362575965b4b291f8ad1c66eb32b5795",
        url="https://pypi.org/packages/ae/0a/7175659da388876dd675c6c816f2a14fd3d1091ce4923d9b17efb02d3a10/jupyterlab-3.1.19-py3-none-any.whl",
    )
    version(
        "3.1.18",
        sha256="3bedbc732ae86b616bd5c7855a6d071fe76ad47186378d36df77f4fc58ae322a",
        url="https://pypi.org/packages/32/e2/577343b7048c5ec6cf6d271dcbd36cb9d12eb0e7111c40e88c90ecd46379/jupyterlab-3.1.18-py3-none-any.whl",
    )
    version(
        "3.1.14",
        sha256="1241ff4ab8604a281eda5d8215fe59e418737edcdfe71df09a0bd5fdd4ccfd2c",
        url="https://pypi.org/packages/a5/83/d4232dc1399a93d5b6f665c92156cf564b25b4d51a641bcdf904796704ee/jupyterlab-3.1.14-py3-none-any.whl",
    )
    version(
        "3.0.18",
        sha256="4a8d2e96711cd35ce0e0c0c826c8991834daf51a2e7f7908413cdeace4fc13f3",
        url="https://pypi.org/packages/5f/ef/59d2f9358e232376806f50ae96cd97fc4eb33f04850a38d846c2727c4d49/jupyterlab-3.0.18-py3-none-any.whl",
    )
    version(
        "3.0.16",
        sha256="88f6e7580c15cf731d96495fda362e786753e18d1e3e7e735915862efb602a92",
        url="https://pypi.org/packages/f7/5a/e9a52aea224ae01a3c34732c886389745fbbc14f0374a96d555add1f5034/jupyterlab-3.0.16-py3-none-any.whl",
    )
    version(
        "2.2.7",
        sha256="a0a1882456098d2fab4c241a0b16a1df96c36de1c45bddbf5fc40867e3d9340e",
        url="https://pypi.org/packages/82/bc/8ca618d6a18d49675ad39f544bcd6ad8a9f31a5784d059d7053c8ec3197b/jupyterlab-2.2.7-py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="6663eed77b10d567499ab998eb71dabb510572f7337ec8efc48ed56cd37f9c5f",
        url="https://pypi.org/packages/2f/4a/b25d71392bb6982b7afa05eba1be22556f7e2d852bd5af9a1682da93916f/jupyterlab-2.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@4.0.0-alpha33:")
        depends_on("python@3.7:", when="@3.3.0-alpha2:3,4.0.0-alpha18:4.0.0-alpha32")
        depends_on("py-async-lru@1:", when="@4.0.0-alpha29:")
        depends_on("py-importlib-metadata@4.8.3:", when="@4.0.0-alpha31: ^python@:3.9")
        depends_on("py-importlib-resources@1.4:", when="@4.0.0-alpha24: ^python@:3.8")
        depends_on("py-ipykernel", when="@4.0.0-alpha20:")
        depends_on("py-ipython", when="@3.0.0-alpha5:4.0.0-alpha19")
        depends_on("py-jinja2@3.0.3:", when="@4.0.0-alpha22:")
        depends_on("py-jinja2@2.1:", when="@3.0.15:3.0,3.1.0-alpha5:4.0.0-alpha21")
        depends_on("py-jinja2@2.10:", when="@:3.0.14,3.1:3.1.0-alpha4")
        depends_on("py-jupyter-core", when="@3.0.0-rc7:")
        depends_on("py-jupyter-lsp@2:", when="@4.0.0-alpha37:")
        depends_on("py-jupyter-server@2.4:", when="@4.0.0-beta1:")
        depends_on("py-jupyter-server@1.16:1", when="@3.4")
        depends_on("py-jupyter-server@1.4:1", when="@3.0.9:3.0,3.1.0-alpha4:3.3,4:4.0.0-alpha21")
        depends_on("py-jupyterlab-server@2.19:", when="@4.0.0-alpha33:")
        depends_on(
            "py-jupyterlab-server@2.10:",
            when="@3.3.0-alpha2:3.6.0-rc0,4.0.0-alpha19:4.0.0-alpha22",
        )
        depends_on(
            "py-jupyterlab-server@2.3:",
            when="@3.0.9:3.0,3.1.0-alpha4:3.3.0-alpha1,4:4.0.0-alpha18",
        )
        depends_on("py-jupyterlab-server@1.1.5:1", when="@2.2:3.0.0-alpha4")
        depends_on("py-jupyterlab-server@1.1:", when="@2.1:2.1.1")
        depends_on("py-nbclassic", when="@3.4.4:3")
        depends_on("py-nbclassic@0.2.0:0", when="@3.0.0-rc14:3.4.3,4:4.0.0-alpha19")
        depends_on("py-notebook@:6", when="@3.4.4:3")
        depends_on("py-notebook@4.3.1:", when="@:3.0.0-alpha4")
        depends_on("py-notebook-shim@0.2:", when="@4.0.0-alpha31:")
        depends_on("py-packaging", when="@3.0.0-beta6:")
        depends_on("py-tomli", when="@3.6.0-alpha3:3,4.0.0-alpha31: ^python@:3.10")
        depends_on("py-tomli", when="@3.4.7:3.6.0-alpha2,4.0.0-alpha27:4.0.0-alpha30")
        depends_on("py-tornado@6.2:", when="@4.0.0-alpha33:")
        depends_on("py-tornado@6.1:", when="@3.0.0-rc14:4.0.0-alpha32")
        depends_on("py-tornado@:6.0-beta1,6.0.3:", when="@:3.0.0-rc13")
        depends_on("py-traitlets", when="@4.0.0-alpha29:")

    # under [tool.hatch.build.hooks.jupyter-builder] in pyproject.toml

    def setup_run_environment(self, env):
        env.set("JUPYTERLAB_DIR", self.prefix.share.jupyter.lab)
