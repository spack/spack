# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEditables(PythonPackage):
    """A Python library for creating "editable wheels"."""

    homepage = "https://github.com/pfmoore/editables"
    pypi = "editables/editables-0.3.tar.gz"

    version(
        "0.3",
        sha256="ee686a8db9f5d91da39849f175ffeef094dd0e9c36d6a59a2e8c7f92a3b80020",
        url="https://pypi.org/packages/ef/8c/87276afb1ba3193c4c05be83965a1e69b8a14821ce6d688464071b179383/editables-0.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3:")
