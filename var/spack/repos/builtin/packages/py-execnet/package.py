# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExecnet(PythonPackage):
    """execnet provides a share-nothing model with channel-send/receive
    communication for distributing execution across many Python interpreters
    across version, platform and network barriers."""

    homepage = "https://codespeak.net/execnet"
    pypi = "execnet/execnet-1.7.1.tar.gz"

    license("MIT")

    version(
        "1.9.0",
        sha256="a295f7cc774947aac58dde7fdc85f4aa00c42adf5d8f5468fc630c1acf30a142",
        url="https://pypi.org/packages/81/c0/3072ecc23f4c5e0a1af35e3a222855cfd9c80a1a105ca67be3b6172637dd/execnet-1.9.0-py2.py3-none-any.whl",
    )
    version(
        "1.7.1",
        sha256="d4efd397930c46415f62f8a31388d6be4f27a91d7550eb79bc64a756e0056547",
        url="https://pypi.org/packages/d3/2e/c63af07fa471e0a02d05793c7a56a9f7d274a8489442a5dc4fb3b2b3c705/execnet-1.7.1-py2.py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="d2b909c7945832e1c19cfacd96e78da68bdadc656440cfc7dfe59b766744eb8c",
        url="https://pypi.org/packages/07/16/51d99ff02e7b03dfdf407b05c157b8d578e23fb0404a640c0ef57ce708e9/execnet-1.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-apipkg@1.4:", when="@1.4:1.8")
