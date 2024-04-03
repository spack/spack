# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServer(PythonPackage):
    """The Jupyter Server provides the backend (i.e. the core services, APIs,
    and REST endpoints) for Jupyter web applications like Jupyter notebook,
    JupyterLab, and Voila."""

    homepage = "https://github.com/jupyter-server/jupyter_server"
    pypi = "jupyter_server/jupyter_server-1.9.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.6.0",
        sha256="19525a1515b5999618a91b3e99ec9f6869aa8c5ba73e0b6279fcda918b54ba36",
        url="https://pypi.org/packages/6f/04/b2e87b4ee96a2219df7666706b28c9ebffd9895fc98fe4b5c56b8b6931ce/jupyter_server-2.6.0-py3-none-any.whl",
    )
    version(
        "1.21.0",
        sha256="992531008544d77e05a16251cdfbd0bdff1b1efa14760c79b9cc776ac9214cf1",
        url="https://pypi.org/packages/0a/87/13dda7b92c48931b9fc006801edc3590b72502ffd95ccc6397c0a64edb91/jupyter_server-1.21.0-py3-none-any.whl",
    )
    version(
        "1.18.1",
        sha256="022759b09c96a4e2feb95de59ce4283e04e17782efe197b91d23a47521609b77",
        url="https://pypi.org/packages/36/6c/fe8c416a9f1a64b9296918e9096b68da81fc50e5fefba8077841c22d6691/jupyter_server-1.18.1-py3-none-any.whl",
    )
    version(
        "1.17.0",
        sha256="5aa5e0945e3dbf29390cfe9c418a9af245d812ce282932ae97d0671e10c147a0",
        url="https://pypi.org/packages/24/93/bf76a457fbe3adc4000c039013e6d1715ae2972eb3f341bb50a1712f8105/jupyter_server-1.17.0-py3-none-any.whl",
    )
    version(
        "1.13.5",
        sha256="a3eb9d397df2de26134cb24fe7cb5da60ec28b4f8b292e0bdefd450b1f062dd3",
        url="https://pypi.org/packages/02/8b/f7ad0a54cdd07b819dc768eb39cf5f09f522b48ff1d5171551358fffd497/jupyter_server-1.13.5-py3-none-any.whl",
    )
    version(
        "1.11.2",
        sha256="eb247b555f5bdfb4a219d78e86bc8769456a1a712d8e30a4dbe06e3fe7e8a278",
        url="https://pypi.org/packages/42/72/692f8b573af200fad3f5020ec485e41baa28eeb3446bc58307651f40df0f/jupyter_server-1.11.2-py3-none-any.whl",
    )
    version(
        "1.11.1",
        sha256="618aba127b1ff35f50e274b6055dfeff006a6008e94d4e9511c251a2d99131e5",
        url="https://pypi.org/packages/c2/5d/38eacdd6a5d250a64458b55044a873ac25c0f1cc85a3ed0401a8384d31fe/jupyter_server-1.11.1-py3-none-any.whl",
    )
    version(
        "1.11.0",
        sha256="827c134da7a9e09136c2dc2fd16743350970105247f085abfc6ce0432d0c979e",
        url="https://pypi.org/packages/99/1b/6cb192774cac40926f71069073d187e727c3bbc276d2a310ca352755455e/jupyter_server-1.11.0-py3-none-any.whl",
    )
    version(
        "1.10.2",
        sha256="491c920013144a2d6f5286ab4038df6a081b32352c9c8b928ec8af17eb2a5e10",
        url="https://pypi.org/packages/b0/3b/fc133648ef2f296e87ea13dd4709b0ac057fe9abb34c6e9e13731953f25f/jupyter_server-1.10.2-py3-none-any.whl",
    )
    version(
        "1.9.0",
        sha256="1a6bfcf4cd58a84dfe9d3060a76bf98428c08b8a177202fc0cadcec5f7d74090",
        url="https://pypi.org/packages/29/b7/7377d007118f7798b21362a6c0a0bf20c93cdc19345105276a862e1263d6/jupyter_server-1.9.0-py3-none-any.whl",
    )
    version(
        "1.6.1",
        sha256="ce7609d75c624d2e6b6eb9159ef019a0320cc55c3b77795ee295c3eb72a08425",
        url="https://pypi.org/packages/c8/12/05d6ec3576611696acc736dc80f0254f5b98cc19a38449a09f05b5517b52/jupyter_server-1.6.1-py3-none-any.whl",
    )

    variant("typescript", default=False, description="Build the typescript code", when="@1.10.2:1")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2.0.0-rc4:")
        depends_on("python@3.7:", when="@1.13.2:2.0.0-rc3")
        depends_on("py-anyio@3.1:", when="@1.15:1.16,2.2.1:")
        depends_on("py-anyio@3.1:3", when="@1.8:1.13,1.17:2.2.0")
        depends_on("py-anyio@2.0.2:", when="@:1.6.2")
        depends_on("py-argon2-cffi", when="@1.5:")
        depends_on("py-ipython-genutils", when="@:1.15.2")
        depends_on("py-jinja2")
        depends_on("py-jupyter-client@7.4.4:", when="@2.0.0-rc4:")
        depends_on("py-jupyter-client@6.1.12:", when="@1.16:2.0.0-rc3")
        depends_on("py-jupyter-client@6.1.1:", when="@:1.15")
        depends_on("py-jupyter-core@4.12:4,5.1:", when="@1.23.5:1,2.0.1:")
        depends_on("py-jupyter-core@4.7.0:", when="@1.16:1.23.4,2:2.0.0-rc3")
        depends_on("py-jupyter-core@4.6:", when="@1.7.0-alpha2:1.15")
        depends_on("py-jupyter-core@4.4:", when="@:1.7.0-alpha1")
        depends_on("py-jupyter-events@0.6:", when="@2.6:2.10.0")
        depends_on("py-jupyter-server-terminals", when="@2:")
        depends_on("py-nbconvert@6.4.4:", when="@1.16:")
        depends_on("py-nbconvert", when="@:1.15")
        depends_on("py-nbformat@5.3.0:", when="@2.0.0-rc8:")
        depends_on("py-nbformat@5.2:", when="@1.15:2.0.0-rc7")
        depends_on("py-nbformat", when="@:1.13")
        depends_on("py-overrides", when="@2.6:")
        depends_on("py-packaging", when="@1.13.2:")
        depends_on("py-prometheus-client")
        depends_on("py-pywin32", when="@:1.7.0-alpha2 platform=windows")
        depends_on("py-pyzmq@24:", when="@2.0.0-rc4:")
        depends_on("py-pyzmq@17.0.0:", when="@:2.0.0-rc3")
        depends_on("py-requests-unixsocket", when="@1.9:1.11.1")
        depends_on("py-send2trash", when="@:2.7.0")
        depends_on("py-terminado@0.8.3:")
        depends_on("py-tornado@6.2:", when="@2.0.0-rc4:")
        depends_on("py-tornado@6.1:", when="@:2.0.0-rc3")
        depends_on("py-traitlets@5.6:", when="@2.0.1:")
        depends_on("py-traitlets@5.1:", when="@1.16:2.0.0-rc4")
        depends_on("py-traitlets@5.0.0:", when="@1.13.3:1.15")
        depends_on("py-traitlets@4.2.1:", when="@:1.13.2")
        depends_on("py-websocket-client", when="@1.7:")

    # https://github.com/spack/spack/issues/41899

    # under [tool.hatch.build.hooks.jupyter-builder] in pyproject.toml

    # for windows depends_on pywinpty, when='@1.13.2:'
    # py-pywinpty is not in spack and requires the build system maturin

    # old
