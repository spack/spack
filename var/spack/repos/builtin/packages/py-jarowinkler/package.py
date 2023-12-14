# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJarowinkler(PythonPackage):
    """library for fast approximate string matching using Jaro and Jaro-Winkler similarity."""

    homepage = "https://github.com/maxbachmann/JaroWinkler"
    pypi = "jarowinkler/jarowinkler-1.2.3.tar.gz"

    maintainers("LydDeb")

    version("2.0.0", sha256="7cfb5e5caef5d22bae44e9cadcd1ff7313970e70303feff31ff78e8b69c92648")
    version("1.2.3", sha256="af28ea284cfbd1b21b29ff94b759f20e94e4f7c06f424b0b4702e701c2a21668")

    depends_on("python@3.8:", when="@2:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build@0.15.0:", when="@1.2.3", type="build")
    depends_on("py-rapidfuzz-capi@1.0.5", when="@1.2.3:", type="build")
