# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRuff(PythonPackage):
    """An extremely fast Python linter, written in Rust."""

    homepage = "https://beta.ruff.rs/docs"
    pypi = "ruff/ruff-0.0.276.tar.gz"
    git = "https://github.com/astral-sh/ruff.git"

    version("0.0.276", sha256="d456c86eb6ce9225507f24fcc7bf72fa031bb7cc750023310e62889bf4ad4b6a")

    depends_on("py-maturin@1", type="build")
