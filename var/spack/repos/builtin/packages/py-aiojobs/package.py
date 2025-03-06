# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiojobs(PythonPackage):
    """Jobs scheduler for managing background task (asyncio)."""

    homepage = "https://github.com/aio-libs/aiojobs"
    pypi = "aiojobs/aiojobs-1.3.0.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0", checked_by="alecbcs")

    version("1.3.0", sha256="03074c884b3dc388b8d798c0de24ec17d72b2799018497fda8062c0431a494b5")

    variant("aiohttp", default=False, description="Enable aiohttp integration")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@46.4:", type="build")

    depends_on("py-async-timeout@4:", type=("build", "run"), when="^python@:3.10")
    depends_on("py-aiohttp@3.9:", type=("build", "run"), when="+aiohttp")
