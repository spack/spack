# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlight(PythonPackage):
    """A catch-all compile-tool wrapper."""

    homepage = "https://github.com/trailofbits/blight"
    pypi = "blight/blight-0.0.47.tar.gz"

    maintainers("woodruffw")

    version("0.0.47", sha256="eb4a881adb98e03a0a855b95bfcddb0f4b3ca568b00cb45b571f047ae75c5667")

    variant("dev", default=False, description="Install dependencies to help with development")

    depends_on("python@3.7:", type=("build", "run"))

    # In process of changing build backend after 0.0.47 release.
    depends_on("py-setuptools", type="build")

    depends_on("py-click@7.1:8", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-pydantic@1.7:1", type=("build", "run"))

    depends_on("py-flake8", when="+dev", type=("build", "run"))
    depends_on("py-black", when="+dev", type=("build", "run"))
    # blight uses pyproject.toml to configure isort. isort added
    # support in 5.0.0
    depends_on("py-isort@5.0.0:", when="+dev", type=("build", "run"))
    depends_on("py-pytest", when="+dev", type=("build", "run"))
    depends_on("py-pytest-cov", when="+dev", type=("build", "run"))
    depends_on("py-coverage+toml", when="+dev", type=("build", "run"))
    depends_on("py-twine", when="+dev", type=("build", "run"))
    depends_on("py-pdoc3", when="+dev", type=("build", "run"))
    depends_on("py-mypy", when="@0.0.5:+dev", type=("build", "run"))
