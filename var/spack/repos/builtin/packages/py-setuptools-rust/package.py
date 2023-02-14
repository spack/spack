# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsRust(PythonPackage):
    """Setuptools rust extension plugin."""

    homepage = "https://github.com/PyO3/setuptools-rust"
    pypi = "setuptools-rust/setuptools-rust-0.12.1.tar.gz"

    version("1.5.1", sha256="0e05e456645d59429cb1021370aede73c0760e9360bbfdaaefb5bced530eb9d7")
    version("1.4.1", sha256="18ff850831f58ee21d5783825c99fad632da21e47645e9427fd7dec048029e76")
    version("1.2.0", sha256="0a4ada479e8c7e3d8bd7cb56e1a29acc2b2bb98c2325051b0cdcb57d7f056de8")
    version("0.12.1", sha256="647009e924f0ae439c7f3e0141a184a69ad247ecb9044c511dabde232d3d570e")

    # Version 0.10.6 is not available on pypi and can only be found on github
    version(
        "0.10.6",
        sha256="1446d3985e4aaf4cc679fda8a48a73ac1390b627c8ae1bebe7d9e08bb3b33769",
        url="https://github.com/PyO3/setuptools-rust/archive/v0.10.6.tar.gz",
        deprecated=True,
    )

    depends_on("python@3.7:", when="@1.2.0:", type=("build", "run"))
    depends_on("python@3.6:", when="@0.12:", type=("build", "run"))
    depends_on("py-setuptools@62.4:", when="@1.4.0:", type=("build", "run"))
    depends_on("py-setuptools@46.1:", when="@0.11.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm+toml@6.3.2:", when="@1.2.0:1.4.1", type="build")
    depends_on("py-setuptools-scm+toml@3.4.3:", when="@0.11:1.1", type="build")
    depends_on("py-semantic-version@2.8.2:2", when="@1.2.0:", type=("build", "run"))
    depends_on("py-semantic-version@2.6.0:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", when="@1.2.0:", type=("build", "run"))
    depends_on("py-toml@0.9.0:", type=("build", "run"), when="@0.12.1")
    depends_on("rust", type="run")
