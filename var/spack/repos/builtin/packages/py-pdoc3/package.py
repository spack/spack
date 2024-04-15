# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPdoc3(PythonPackage):
    """Auto-generate API documentation for Python projects."""

    homepage = "https://pdoc3.github.io/pdoc/"
    pypi = "pdoc3/pdoc3-0.10.0.tar.gz"

    license("AGPL-3.0")

    version(
        "0.10.0",
        sha256="ba45d1ada1bd987427d2bf5cdec30b2631a3ff5fb01f6d0e77648a572ce6028b",
        url="https://pypi.org/packages/67/36/add16f4705689ed1f31aba24c973d035fc953c6fe54af9143837cc3b1315/pdoc3-0.10.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-mako", when="@0.10:")
        depends_on("py-markdown@3:", when="@0.10:")
