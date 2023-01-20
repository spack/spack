# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyA2wsgi(PythonPackage):
    """Convert WSGI app to ASGI app or ASGI app to WSGI app."""

    homepage = "https://github.com/abersheeran/a2wsgi"
    pypi = "a2wsgi/a2wsgi-1.6.0.tar.gz"

    version("1.6.0", sha256="67a9902db6da72c268a24d4e5d01348f736980a577279b7df801c8902aba8554")

    depends_on("python@3.6.2:", type=("build", "run"))

    depends_on("py-pdm-pep517@1.0.0:", type=("build", "run"))
