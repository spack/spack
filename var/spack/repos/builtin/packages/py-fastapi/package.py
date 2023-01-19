# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastapi(PythonPackage):
    """FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

    homepage = "https://github.com/tiangolo/fastapi"
    pypi = "fastapi/fastapi-0.88.0.tar.gz"

    version("0.88.0", sha256="915bf304180a0e7c5605ec81097b7d4cd8826ff87a02bb198e336fb9f3b5ff02")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-hatchling", type="build")

    depends_on("py-starlette@0.22.0", type=("build", "run"))
    depends_on("py-pydantic@1.6.2:1.6,1.7.4:1.7,1.8.2:1", type=("build", "run"))
