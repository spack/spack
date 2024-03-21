# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRuff(PythonPackage):
    """An extremely fast Python linter, written in Rust."""

    homepage = "https://beta.ruff.rs/docs"
    pypi = "ruff/ruff-0.0.276.tar.gz"
    git = "https://github.com/astral-sh/ruff.git"

    license("MIT")

    version("0.3.0", sha256="0886184ba2618d815067cf43e005388967b67ab9c80df52b32ec1152ab49f53a")
    version("0.1.6", sha256="1b09f29b16c6ead5ea6b097ef2764b42372aebe363722f1605ecbcd2b9207184")
    version(
        "0.0.276",
        sha256="d456c86eb6ce9225507f24fcc7bf72fa031bb7cc750023310e62889bf4ad4b6a",
        deprecated=True,
    )

    depends_on("py-maturin@1", type="build")

    # Found in Cargo.toml
    depends_on("rust@1.71:", when="@0.1.6:", type="build")
    depends_on("rust@1.70:", when="@0.0.276:", type="build")
