# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGleanSdk(PythonPackage):
    """Mozilla's Glean Telemetry SDK"""

    homepage = "https://mozilla.github.io/glean/book/index.html"
    url = "https://files.pythonhosted.org/packages/cc/61/b9ac09a243994a1380ecfb786ede782df9bf31a48136a0a8b1a939604af2/glean_sdk-60.0.1.tar.gz"

    license("MPL-2.0", checked_by="teaguesterling")

    version("60.0.1", sha256="160d054b27b8ef221cfd143b531d120ed0ee6a3d0e858eb80560f56dcfb12f35")

    depends_on("python@3.8:")
    depends_on("py-semver@2.13.0:")
    depends_on("py-glean-parser@14.0")
    depends_on("py-maturin")

