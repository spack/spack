# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuart(PythonPackage):
    """A Python ASGI web microframework with the same API as
    Flask."""

    homepage = "https://gitlab.com/pgjones/quart/"
    pypi = "Quart/Quart-0.16.3.tar.gz"

    version("0.16.3", sha256="16521d8cf062461b158433d820fff509f98fb997ae6c28740eda061d9cba7d5e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-aiofiles", type=("build", "run"))
    depends_on("py-blinker", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-hypercorn@0.11.2:", type=("build", "run"))
    depends_on("py-itsdangerous", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-werkzeug@2:", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.7")
