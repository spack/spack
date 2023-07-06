# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiobotocore(PythonPackage):
    """Async client for amazon services using botocore and aiohttp/asyncio."""

    homepage = "https://aiobotocore.readthedocs.io/en/latest/"
    pypi = "aiobotocore/aiobotocore-1.2.1.tar.gz"

    version("2.5.0", sha256="6a5b397cddd4f81026aa91a14c7dd2650727425740a5af8ba75127ff663faf67")
    version("2.4.2", sha256="0603b74a582dffa7511ce7548d07dc9b10ec87bc5fb657eb0b34f9bd490958bf")
    version("1.2.1", sha256="58cc422e65fc89f7cb78eca740d241ac8e15f39f6b308cc23152711e8a987d45")

    depends_on("py-setuptools", type="build")
    depends_on("py-botocore@1.27.59", when="@2.4.2", type=("build", "run"))
    depends_on("py-botocore@1.19.52", when="@1.2.1", type=("build", "run"))
    depends_on("py-botocore@1.29.76", when="@2.5.0", type=("build", "run"))
    depends_on("py-aiohttp@3.3.1:", type=("build", "run"))
    depends_on("py-wrapt@1.10.10:", type=("build", "run"))
    depends_on("py-aioitertools@0.5.1:", type=("build", "run"))
