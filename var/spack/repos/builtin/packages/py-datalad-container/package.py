# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladContainer(PythonPackage):
    """DataLad extension package for working with containerized environments"""

    homepage = "https://github.com/datalad/datalad-container/"
    pypi = "datalad_container/datalad_container-1.1.5.tar.gz"

    license("MIT")

    version(
        "1.2.0",
        sha256="c42e1f0b475dae866f82545e6f39ef2e45572d05a1341aa7e6ff8135935e3863",
        url="https://pypi.org/packages/d6/f3/3f9f50fba9d9c4f37ef2effb7f22d44014aedc7f480582934a3c6d78d8c3/datalad_container-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.7",
        sha256="0a628b21ad1145ba3512eee2d8cf49196a1dce344a6f35782a44b1eb7f9fa588",
        url="https://pypi.org/packages/1c/24/bf1e49b6bde41e09d6c5cb951c4540c21b2cef3075431f00f32a05b43845/datalad_container-1.1.7-py3-none-any.whl",
    )
    version(
        "1.1.5",
        sha256="5b4f40edb781c95f7bf91091894bb73b920531dabb7e5a3b9b79ee118b6097cb",
        url="https://pypi.org/packages/a2/7f/e615773bd6a1a54ab3ec868d3eefe2f3ce841b04278fe7e44333875b698c/datalad_container-1.1.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.1.6:")
        depends_on("py-datalad@0.18:", when="@1.1.9:")
        depends_on("py-datalad@0.13.0:", when="@1.1:1.1.8")
        depends_on("py-requests@1.2:", when="@0.5.1:0,1.0.1:")
