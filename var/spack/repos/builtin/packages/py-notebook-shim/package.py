# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNotebookShim(PythonPackage):
    """A shim layer for notebook traits and config."""

    homepage = "https://github.com/jupyter/notebook_shim"
    pypi = "notebook_shim/notebook_shim-0.2.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.2.3",
        sha256="a83496a43341c1674b093bfcebf0fe8e74cbe7eda5fd2bbc56f8e39e1486c0c7",
        url="https://pypi.org/packages/f4/79/73250372e5bbab63018b41b02d5cc6b395655ec6c1254e477ef7c913aada/notebook_shim-0.2.3-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="9c6c30f74c4fbea6fce55c1be58e7fd0409b1c681b075dcedceb005db5026949",
        url="https://pypi.org/packages/29/34/b3d57a23287c55fe964da403bb5457baacc2c0edc1fc3bf2739d4a958d90/notebook_shim-0.2.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.1:")
        depends_on("py-jupyter-server@1.8:", when="@0.2:")
