# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMeshio(PythonPackage):
    """MeshIO is a Python library to read and write many mesh formats."""

    homepage = "https://github.com/nschloe/meshio"
    pypi = "meshio/meshio-5.0.0.tar.gz"

    license("MIT")

    version(
        "5.0.1",
        sha256="c595bb11869dda9afb3945d30f455c58ccf4807987e6797ebbf185793513b970",
        url="https://pypi.org/packages/f3/55/82043c45c04c01dbf230e12a9de06f7eac4215caa7bdd7096537cf7dd59e/meshio-5.0.1-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="c166ede5dce301da45dcd7652156bd123a5032b153f1f2cb1653047c3ae02db4",
        url="https://pypi.org/packages/0f/bd/ecff2af49fe5a1413cb9d42f87f61e1a399358041c74ffa4839a4ecf7446/meshio-5.0.0-py3-none-any.whl",
    )
    version(
        "4.4.6",
        sha256="ac77a066584265d3426d01bd0fde9e99c47c35340a32d23790ccd22aa566cd75",
        url="https://pypi.org/packages/bb/36/02702cfc5fdf19e6477ea2a78cac4a774a8da4c2cf9557f3ddfb33c74192/meshio-4.4.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5:5.3.4")
        depends_on("py-importlib-metadata", when="^python@:3.7")
        depends_on("py-numpy", when="@:5.3.4")
