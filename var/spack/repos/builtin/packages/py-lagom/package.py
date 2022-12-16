# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyLagom(PythonPackage):
    """Lagom is a dependency injection container
    designed to give you 'just enough' help with building your dependencies.
    """

    homepage = "https://lagom-di.readthedocs.io"

    if sys.platform == "darwin":
        version(
            "2.2.0-cp311",
            url="https://files.pythonhosted.org/packages/6d/cc/9bb100c5a4b400bc1a3612d3796479225c4f228f48806073cfe552b04c61/lagom-2.2.0-cp311-cp311-macosx_10_9_x86_64.whl",
            sha256="e4b866945c2c5718b9a646417bee8ed7f6268d4c7ef2ce13a6fa5a26cd44e059",
            expand=False,
        )
        version(
            "2.2.0-cp310",
            url="https://files.pythonhosted.org/packages/ea/ba/6ab3d454c430f2f474ba008b5ba10576b74a326c3a1ec09b182d0bd23d67/lagom-2.2.0-cp310-cp310-macosx_10_9_x86_64.whl",
            sha256="2a84397581307f2a7f7d673c06440f74811a8bc3756a2a5a162f9e54cf9d405b",
            expand=False,
        )
        version(
            "2.2.0-cp39",
            url="https://files.pythonhosted.org/packages/30/31/a497d4df99943ef917a9f32996ee94f28eab754e4e3518ea9547a0d737f0/lagom-2.2.0-cp39-cp39-macosx_10_9_x86_64.whl",
            sha256="73fc974518264bcd380bfd0882b87d69db89b525a7d93c1fae086a481c1f2177",
            expand=False,
        )
        version(
            "2.2.0-cp38",
            url="https://files.pythonhosted.org/packages/42/6b/d4265f6c9af605b15b6f73b34da0475fcf94c8b2c88a09ec8c0ac0a38d3b/lagom-2.2.0-cp38-cp38-macosx_10_9_x86_64.whl",
            sha256="f0470096acde88625ae034c5cbd7d744f45bc0dc8092ecc0a3256244f1ec9a4d",
            expand=False,
        )
        version(
            "2.2.0-cp37",
            url="https://files.pythonhosted.org/packages/8f/70/01bff345884c56dc6376e08640544fa6544060f737897a003d921ec338b2/lagom-2.2.0-cp37-cp37m-macosx_10_9_x86_64.whl",
            sha256="cb9e11a7f2a5cd13452e8f7f7df8fa36fe1703fef9d4d72e70339f19ca3b2b8d",
            expand=False,
        )
    else:
        version(
            "2.2.0-cp311",
            url="https://files.pythonhosted.org/packages/a3/03/da85e7d41b5883fbffd0eb5a84280f0ee3736225359a1305e0c97b0221e0/lagom-2.2.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            sha256="b9744afa26e93a0e031f2653aed279a3ca7aaff9fed242d0e28b108ffc7ed2ef",
            expand=False,
        )
        version(
            "2.2.0-cp310",
            url="https://files.pythonhosted.org/packages/6e/7f/1552f6be17dcbccfb05a32d9fd363aa5d080512a9faabf20ce865108907c/lagom-2.2.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            sha256="0d5d50e81d2d37e13fbb5ca656b5fe8e1c883954b7ecd2bcd963fc8a5a0422c4",
            expand=False,
        )
        version(
            "2.2.0-cp39",
            url="https://files.pythonhosted.org/packages/ba/70/aad167bc50165b40c6b2334de96a24a1573cf26a91688bf1bb81b98c8347/lagom-2.2.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            sha256="338c7c59dff4dba471e4455ba5acabf3229f1e85e868ce26b4d87d9f25c781f2",
            expand=False,
        )
        version(
            "2.2.0-cp38",
            url="https://files.pythonhosted.org/packages/00/16/61e58a1d7a7f796dc4400f990697323170b5aa528f6d969ad3c2b0c09eb6/lagom-2.2.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            sha256="a3dea612d94e3e3a65df42244a4124a3a0e03c0e25b11e66f7242e2ef349b0f6",
            expand=False,
        )
        version(
            "2.2.0-cp37",
            url="https://files.pythonhosted.org/packages/b6/99/89566922e79fc08d1a5d875cce2da616f89fef6b91547164828f1e3fe6d9/lagom-2.2.0-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            sha256="72c9f67d31df72e83885d9c74a81a20ff3f988a6de119248f6964d3a747e7aa9",
            expand=False,
        )

    depends_on("python@3.11.0:3.11", when="@2.2.0-cp311", type=("build", "run"))
    depends_on("python@3.10.0:3.10", when="@2.2.0-cp310", type=("build", "run"))
    depends_on("python@3.9.0:3.9", when="@2.2.0-cp39", type=("build", "run"))
    depends_on("python@3.8.0:3.8", when="@2.2.0-cp38", type=("build", "run"))
    depends_on("python@3.7.0:3.7", when="@2.2.0-cp37", type=("build", "run"))

    depends_on("py-setuptools", type="build")
