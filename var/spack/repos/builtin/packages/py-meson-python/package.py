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

    # Needed for py-scikit-image, deprecate and remove once 0.13.0 is officially released
    version("0.13.1", sha256="63b3170001425c42fa4cfedadb9051cbd28925ff8eed7c40d36ba0099e3c7618")
    version(
        "0.13.0.pre0",
        sha256="8d537a0304709c31c11ffa34872a62a4c06a6a6c24fc862b7fb4306f3e881b95",
        deprecated=True,
    )
    version("0.12.0", sha256="8cb159a8093a2e73cfa897f8092ec93b74e3842f94dff7fde381c6fe0e0b064d")
    version("0.11.0", sha256="110258837c2ffe762f5f855c7ea5385f1edd44074e93a0f317ffefc7aab42b09")
    version("0.10.0", sha256="08dd122c1074dbd5c55b53993a719cca73dd8216372c91217f7a550260f9e7e1")
    version("0.9.0", sha256="6aa5a09ff5cce1c5308938ebbf3eab5529413c8677055ace1ac8c83d8a07b29d")
    version("0.8.1", sha256="442f1fa4cf5db50eea61170a6059c10fafd70977f5dbdf3441c106cd23b05e4c")
    version("0.8.0", sha256="b5c8a2727e6f6feaffc1db513244c9bdb5d0f689b45e24f4529b649b7710daf7")
    version("0.7.0", sha256="9fcfa350f44ca80dd4f5f9c3d251725434acf9a07d9618f382e6cc4629dcbe84")

    depends_on("py-colorama", when="platform=windows", type=("build", "run"))
    depends_on("meson@0.63.3:", when="@0.11:", type=("build", "run"))
    depends_on("meson@0.63:", when="@0.9:0.10", type=("build", "run"))
    depends_on("meson@0.62:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.7.1:", when="@0.13:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.6.1:", when="@0.12:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.5:", type=("build", "run"))
    depends_on("py-tomli@1:", when="@0.11: ^python@:3.10", type=("build", "run"))
    depends_on("py-tomli@1:", when="@:0.10", type=("build", "run"))
    depends_on("py-setuptools@60:", when="@0.13: ^python@3.12:", type=("build", "run"))

    # https://github.com/mesonbuild/meson-python/pull/111
    conflicts("platform=darwin os=ventura", when="@:0.7")
    conflicts("platform=darwin os=monterey", when="@:0.7")
    conflicts("platform=darwin os=bigsur", when="@:0.7")

    # Historical dependencies
    depends_on("py-typing-extensions@3.7.4:", when="@0.12 ^python@:3.9", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@:0.11 ^python@:3.7", type=("build", "run"))
