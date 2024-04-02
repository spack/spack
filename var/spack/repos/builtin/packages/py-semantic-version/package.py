# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySemanticVersion(PythonPackage):
    """This small python library provides a few tools to handle SemVer in
    Python. It follows strictly the 2.0.0 version of the SemVer scheme."""

    homepage = "https://github.com/rbarrois/python-semanticversion"
    pypi = "semantic_version/semantic_version-2.8.2.tar.gz"

    license("BSD-2-Clause")

    version(
        "2.10.0",
        sha256="de78a3b8e0feda74cabc54aab2da702113e33ac9d9eb9d2389bcf1f58b7d9177",
        url="https://pypi.org/packages/6a/23/8146aad7d88f4fcb3a6218f41a60f6c2d4e3a72de72da1825dc7c8f7877c/semantic_version-2.10.0-py2.py3-none-any.whl",
    )
    version(
        "2.9.0",
        sha256="db2504ab37902dd2c9876ece53567aa43a5b2a417fbe188097b2048fff46da3d",
        url="https://pypi.org/packages/64/ac/df31047966c4d0293e7bd16276ebc9f6654de36ad8e19061a09369380c0a/semantic_version-2.9.0-py2.py3-none-any.whl",
    )
    version(
        "2.8.5",
        sha256="45e4b32ee9d6d70ba5f440ec8cc5221074c7f4b0e8918bdab748cc37912440a9",
        url="https://pypi.org/packages/a5/15/00ef3b7888a10363b7c402350eda3acf395ff05bebae312d1296e528516a/semantic_version-2.8.5-py2.py3-none-any.whl",
    )
    version(
        "2.8.2",
        sha256="695d5a06a86439d2dd0e5eaf3e46c5e6090bb5e72ba88377680a0acb483a3b44",
        url="https://pypi.org/packages/0f/3b/8fee26649a86c71df159ed0ae7ac5f9ac38829bccd8a7404e116f903929b/semantic_version-2.8.2-py2.py3-none-any.whl",
    )
    version(
        "2.6.0",
        sha256="2d06ab7372034bcb8b54f2205370f4aa0643c133b7e6dbd129c5200b83ab394b",
        url="https://pypi.org/packages/28/be/3a7241d731ba89063780279a5433f5971c1cf41735b64a9f874b7c3ff995/semantic_version-2.6.0-py3-none-any.whl",
    )
