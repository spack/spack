# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonMarkdownMath(PythonPackage):
    """Math extension for Python-Markdown"""

    pypi = "python-markdown-math/python-markdown-math-0.8.tar.gz"

    maintainers("wscullin")

    license("BSD-3-Clause")

    version(
        "0.8",
        sha256="c685249d84b5b697e9114d7beb352bd8ca2e07fd268fd4057ffca888c14641e5",
        url="https://pypi.org/packages/4d/36/d16118345ff5f503d4d1c708e8427ed2213f2af7aaffac9d59010e665b5c/python_markdown_math-0.8-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-markdown@3:", when="@0.7:")
