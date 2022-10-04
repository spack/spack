# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomli(PythonPackage):
    """Tomli is a Python library for parsing TOML.

    Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    pypi = "https://pypi.org/project/tomli/"
    git = "https://github.com/hukkin/tomli.git"

    version(
        "2.0.1",
        sha256="939de3e7a6161af0c887ef91b7d41a53e7c5a1ca976325f429cb46ea9bc30ecc",
        expand=False,
    )
    version(
        "1.2.2",
        sha256="f04066f68f5554911363063a30b108d2b5a5b1a010aa8b6132af78489fe3aade",
        expand=False,
    )
    version(
        "1.2.1",
        sha256="8dd0e9524d6f386271a36b41dbf6c57d8e32fd96fd22b6584679dc569d20899f",
        expand=False,
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.7:", when="@2.0.1:", type=("build", "run"))
