# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGleanSdk(PythonPackage):
    """Mozilla's Glean Telemetry SDK"""

    homepage = "https://mozilla.github.io/glean/book/index.html"
    url = "https://github.com/mozilla/glean/archive/refs/tags/v60.4.0.tar.gz"

    license("MPL-2.0", checked_by="teaguesterling")

    version("60.4.0", sha256="24bc608e06580962ce029cc4c09a51af75e4a29b3d889232b298f87208acbf62")
    version("60.0.1", sha256="160d054b27b8ef221cfd143b531d120ed0ee6a3d0e858eb80560f56dcfb12f35")

    depends_on("python@3.8:")
    depends_on("py-semver@2.13.0:")
    depends_on("py-glean-parser@14.0", when="@:60.3")
    depends_on("py-glean-parser@14.3:", when="@60.4:")
    depends_on("py-maturin@1")
