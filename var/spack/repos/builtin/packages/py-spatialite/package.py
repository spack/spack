# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpatialite(PythonPackage):
    """Wrapper for standard Python module "sqlite3" which adds SpatiaLite
    support.
    """

    homepage = "https://github.com/malexer/spatialite"
    pypi = "spatialite/spatialite-0.0.3.tar.gz"

    license("MIT")

    version(
        "0.0.3",
        sha256="3124f643688c8ba4e2ff200ef401cf7b57caa44db666cb78519784f98f662982",
        url="https://pypi.org/packages/43/5d/ff0c1c7ca9b4d294029f9a2a2a2f668e8e33e7926135d7a86c35d855eb23/spatialite-0.0.3-py3-none-any.whl",
    )
