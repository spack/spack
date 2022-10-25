# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMesonPython(PythonPackage):
    """Meson Python build backend (PEP 517)."""

    homepage = "https://github.com/FFY00/mesonpy"
    pypi = "meson_python/meson_python-0.7.0.tar.gz"

    maintainers = ["eli-schwartz", "adamjstewart"]

    version("0.10.0", sha256="08dd122c1074dbd5c55b53993a719cca73dd8216372c91217f7a550260f9e7e1")
    version("0.9.0", sha256="6aa5a09ff5cce1c5308938ebbf3eab5529413c8677055ace1ac8c83d8a07b29d")
    version("0.8.1", sha256="442f1fa4cf5db50eea61170a6059c10fafd70977f5dbdf3441c106cd23b05e4c")
    version("0.8.0", sha256="b5c8a2727e6f6feaffc1db513244c9bdb5d0f689b45e24f4529b649b7710daf7")
    version("0.7.0", sha256="9fcfa350f44ca80dd4f5f9c3d251725434acf9a07d9618f382e6cc4629dcbe84")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("meson@0.63:", when="@0.9:", type=("build", "run"))
    depends_on("meson@0.62:", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.5:", type=("build", "run"))
    depends_on("py-tomli@1:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-colorama", when="platform=windows", type=("build", "run"))

    # https://github.com/FFY00/meson-python/pull/111
    conflicts("platform=darwin os=ventura", when="@:0.7")
    conflicts("platform=darwin os=monterey", when="@:0.7")
    conflicts("platform=darwin os=bigsur", when="@:0.7")
