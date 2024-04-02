# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRoutes(PythonPackage):
    """Routing Recognition and Generation Tools"""

    homepage = "https://routes.readthedocs.io/"
    pypi = "routes/Routes-2.5.1.tar.gz"

    license("MIT")

    version(
        "2.5.1",
        sha256="fab5a042a3a87778eb271d053ca2723cadf43c95b471532a191a48539cb606ea",
        url="https://pypi.org/packages/9b/d4/d3c7d029de6287ff7bd048e628920d4336b4f8d82cfc00ff078bdbb212a3/Routes-2.5.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-repoze-lru@0.3:", when="@2.4:")
        depends_on("py-six", when="@2.4:")
