# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWaitress(PythonPackage):
    """Waitress: a production-quality pure-Python WSGI server with very acceptable performance."""

    homepage = "https://github.com/Pylons/waitress/"
    pypi = "waitress/waitress-2.1.2.tar.gz"

    license("ZPL-2.1")

    version("2.1.2", sha256="780a4082c5fbc0fde6a2fcfe5e26e6efc1e8f425730863c04085769781f51eba")

    depends_on("py-setuptools@41:", type="build")
