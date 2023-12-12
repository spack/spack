# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMesonPython(PythonPackage):
    """Meson Python build backend (PEP 517)."""

    homepage = "https://github.com/mesonbuild/meson-python"
    pypi = "meson_python/meson_python-0.7.0.tar.gz"

    maintainers("eli-schwartz", "adamjstewart", "rgommers")

    version("0.13.1", sha256="63b3170001425c42fa4cfedadb9051cbd28925ff8eed7c40d36ba0099e3c7618")
    version("0.12.0", sha256="8cb159a8093a2e73cfa897f8092ec93b74e3842f94dff7fde381c6fe0e0b064d")
    version("0.11.0", sha256="110258837c2ffe762f5f855c7ea5385f1edd44074e93a0f317ffefc7aab42b09")

    depends_on("py-colorama", when="platform=windows", type=("build", "run"))
    depends_on("meson@0.63.3:", when="@0.11:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.7.1:", when="@0.13:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.6.1:", when="@0.12:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.5:", type=("build", "run"))
    depends_on("py-tomli@1:", when="@0.11: ^python@:3.10", type=("build", "run"))
    depends_on("py-setuptools@60:", when="@0.13: ^python@3.12:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-typing-extensions@3.7.4:", when="@0.12 ^python@:3.9", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@:0.11 ^python@:3.7", type=("build", "run"))
