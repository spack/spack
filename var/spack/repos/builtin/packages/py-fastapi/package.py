# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastapi(PythonPackage):
    """FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

    homepage = "https://github.com/tiangolo/fastapi"
    pypi = "fastapi/fastapi-0.88.0.tar.gz"

    license("MIT")

    version(
        "0.98.0",
        sha256="f4165fb1fe3610c52cb1b8282c1480de9c34bc270f56a965aa93a884c350d605",
        url="https://pypi.org/packages/50/2c/6b94f191519dcc8190e78aff7bcb12c58329d1ab4c8aa11f2def9c214599/fastapi-0.98.0-py3-none-any.whl",
    )
    version(
        "0.88.0",
        sha256="263b718bb384422fe3d042ffc9a0c8dece5e034ab6586ff034f6b4b1667c3eee",
        url="https://pypi.org/packages/d8/09/ce090f6d53ce8b6335954488087210fa1e054c4a65f74d5f76aed254c159/fastapi-0.88.0-py3-none-any.whl",
    )

    variant("all", default=False, description="Build all optional dependencies")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.84:0.103")
        depends_on("py-email-validator@1.1.1:", when="@0.87:0.99+all")
        depends_on("py-httpx@0.23:", when="@0.87:+all")
        depends_on("py-itsdangerous@1:", when="@0.87:+all")
        depends_on("py-jinja2@2.11.2:", when="@0.87:+all")
        depends_on("py-orjson@3.2.1:", when="@0.87:+all")
        depends_on("py-pydantic@1.7.4:1.7,1.8.2:1", when="@0.96.1:0.99")
        depends_on("py-pydantic@1.6.2:1.6,1.7.4:1.7,1.8.2:1", when="@:0.96.0")
        depends_on("py-python-multipart@0.0.5:", when="@0.87:0.109.0+all")
        depends_on("py-pyyaml@5.3.1:", when="@0.87:+all")
        depends_on("py-starlette@0.27", when="@0.95.2:0.106")
        depends_on("py-starlette@0.22", when="@0.88:0.89")
        depends_on("py-ujson@4.0.1,5.2:", when="@0.87:+all")
        depends_on("py-uvicorn@0.12:+standard", when="@0.87:+all")

    conflicts("^py-pydantic@1.7.0:1.7.3,1.8.0:1.8.1")
