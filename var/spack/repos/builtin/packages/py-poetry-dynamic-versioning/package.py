# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryDynamicVersioning(PythonPackage):
    """Plugin for Poetry to enable dynamic versioning based on VCS tags."""

    homepage = "https://github.com/mtkennerly/poetry-dynamic-versioning"
    pypi = "poetry-dynamic-versioning/poetry-dynamic-versioning-0.19.0.tar.gz"

    version("0.19.0", sha256="a11a7eba6e7be167c55a1dddec78f52b61a1832275c95519ad119c7a89a7f821")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")

    depends_on("py-dunamai@1.12:1", type=("build", "run"))
    depends_on("py-tomlkit@0.4:", type=("build", "run"))
    depends_on("py-jinja2@2.11.1:3", type=("build", "run"))
