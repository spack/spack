# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiofiles(PythonPackage):
    """aiofiles is an Apache2 licensed library, written in Python, for
    handling local disk files in asyncio applications."""

    homepage = "https://github.com/Tinche/aiofiles"
    pypi = "aiofiles/aiofiles-0.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.7.0",
        sha256="c67a6823b5f23fcab0a2595a289cec7d8c863ffcb4322fb8cd6b90400aedfdbc",
        url="https://pypi.org/packages/e7/61/007ac6f27fe1c2dc44d3a62f429a8440de1601428b4d0291eae1a3494d1f/aiofiles-0.7.0-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="377fdf7815cc611870c59cbd07b68b180841d2a2b79812d8c218be02448c2acb",
        url="https://pypi.org/packages/f4/2b/078a9771ae4b67e36b0c2a973df845260833a4eb088b81c84b738509b4c4/aiofiles-0.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@0.7:0")

    # Historical dependencies
