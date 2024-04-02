# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningCloud(PythonPackage):
    """Lightning AI Command Line Interface."""

    homepage = "https://lightning.ai/"
    pypi = "lightning_cloud/lightning_cloud-0.5.31.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.38",
        sha256="cd783977f46cfa41791747307f0b1f7772d6a6315b3a5bbef565b3537d0b5070",
        url="https://pypi.org/packages/7b/1e/9c34fc7b9aaf0d55815638b800f1f0205c39ab99e000fdc80e0b57c3463f/lightning_cloud-0.5.38-py3-none-any.whl",
    )
    version(
        "0.5.37",
        sha256="2556d1294b23f3cc3f047acd62cd0a26c2daa84896b0c34e46fa6b2a142848db",
        url="https://pypi.org/packages/03/2f/33b90917267b414ba46d8899920a0ac5b8f0686c5c4d1365b52cea7baccc/lightning_cloud-0.5.37-py3-none-any.whl",
    )
    version(
        "0.5.36",
        sha256="9932a5c8c7373eb698a98f3c24380c6452968dc53af75564fc19dda1dd005000",
        url="https://pypi.org/packages/fe/76/a19b6bd5df98dcd2afc1e43c7fb7407176c74094a76e471e3c57a0e2c9cd/lightning_cloud-0.5.36-py3-none-any.whl",
    )
    version(
        "0.5.31",
        sha256="38d87d41ff26436eea803443ae0ea4b64c1b5a3878be7f93895929bcda7ac69f",
        url="https://pypi.org/packages/e7/3f/1db43298149f607244551efb07ec8751358477986da23dbd56bd89724a72/lightning_cloud-0.5.31-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-click")
        depends_on("py-fastapi", when="@0.5.33:")
        depends_on("py-fastapi+all", when="@:0.5.32")
        depends_on("py-pyjwt")
        depends_on("py-python-multipart", when="@0.5.33:")
        depends_on("py-requests")
        depends_on("py-rich")
        depends_on("py-six")
        depends_on("py-urllib3")
        depends_on("py-uvicorn", when="@0.5.33:")
        depends_on("py-websocket-client")

    # requirements.txt
