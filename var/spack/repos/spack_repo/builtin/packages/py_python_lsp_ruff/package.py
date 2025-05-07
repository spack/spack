# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLspRuff(PythonPackage):
    """A plugin for python-lsp-server that adds linting, code action and
    formatting capabilities that are provided by ruff, an extremely fast Python
    linter and formatter written in Rust.
    """

    homepage = "https://github.com/python-lsp/python-lsp-ruff"
    pypi = "python_lsp_ruff/python_lsp_ruff-2.2.2.tar.gz"
    git = "https://github.com/python-lsp/python-lsp-ruff.git"

    maintainers("alecbcs")

    license("MIT")

    version("main", branch="main")
    version("2.2.2", sha256="3f80bdb0b4a8ee24624596a1cff60b28cc37771773730f9bf7d946ddff9f0cac")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-ruff@0.2.0:", type=("build", "run"))
    depends_on("py-cattrs", type=("build", "run"))
    depends_on("py-python-lsp-server", type=("build", "run"))
    depends_on("py-lsprotocol@2023.0.1:", type=("build", "run"))
    depends_on("py-tomli@1.1.0:", type=("build", "run"), when="^python@:3.10")

    conflicts("^py-cattrs@23.2.1", when="@2.2.2")
