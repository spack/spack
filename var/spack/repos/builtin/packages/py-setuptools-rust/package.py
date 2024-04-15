# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsRust(PythonPackage):
    """Setuptools rust extension plugin."""

    homepage = "https://github.com/PyO3/setuptools-rust"
    pypi = "setuptools-rust/setuptools-rust-0.12.1.tar.gz"

    license("MIT")

    version(
        "1.6.0",
        sha256="e28ae09fb7167c44ab34434eb49279307d611547cb56cb9789955cdb54a1aed9",
        url="https://pypi.org/packages/57/db/7cc20ad859bc2a6a0c60e497c4be19784a8d14ff8e53a6da6ee4a6edd500/setuptools_rust-1.6.0-py3-none-any.whl",
    )
    version(
        "1.5.1",
        sha256="306b236ff3aa5229180e58292610d0c2c51bb488191122d2fc559ae4caeb7d5e",
        url="https://pypi.org/packages/5b/76/6ebf4728d287527514b29bc92c14ec59f666f43b0af650df6c100614c3dc/setuptools_rust-1.5.1-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="12b5350d75008f2d4b64a991aba0358bb7ef45502bad086990b019a760afec67",
        url="https://pypi.org/packages/c4/d3/b101f6af5d70988a89fa2b5d7f0d9bc92974014e3eb61ee3802966dc07a6/setuptools_rust-1.4.1-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="decc6bdf4aef0ff3c323ba85e2fcabed8c77044443cd239ea01b67ca9b1d777e",
        url="https://pypi.org/packages/3e/92/7d8e368c14284ff7dc7df5bf55883f0841a1f7cbcae5517417379c46718f/setuptools_rust-1.2.0-py3-none-any.whl",
    )
    version(
        "0.12.1",
        sha256="60c9bf1423a725e472c4a2a6274598251f959f3ed5ffe7698526e78bb431b9b7",
        url="https://pypi.org/packages/82/2b/349ad916a2f032506a2c7c0810950a299f96e05d88b21797c2170bd6b2c6/setuptools_rust-0.12.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1.2:1.7")
        depends_on("py-semantic-version@2.8.2:", when="@1:")
        depends_on("py-semantic-version@2.6:", when="@:0")
        depends_on("py-setuptools@62.4:", when="@1.4:")
        depends_on("py-setuptools@46.1:", when="@0.12:1.2")
        depends_on("py-toml@0.9:", when="@:0")
        depends_on("py-typing-extensions@3.7.4.3:", when="@1:1.7")

    # <<< manual changes
    depends_on("rust", type="run")
    # manual changes >>>
