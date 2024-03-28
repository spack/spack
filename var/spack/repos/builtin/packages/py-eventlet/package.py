# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEventlet(PythonPackage):
    """Concurrent networking library for Python"""

    homepage = "https://github.com/eventlet/eventlet"
    url = "https://github.com/eventlet/eventlet/releases/download/v0.22.0/eventlet-0.22.0.tar.gz"

    license("MIT")

    version(
        "0.22.0",
        sha256="834daff4e296f23472e2125429e72bb6f4e2721b373a911c62d48f8f736215c2",
        url="https://pypi.org/packages/79/d7/946d858c453bc92ef4f4da7a920c4487faf2d6e3d772eaf0087e5f31c5cb/eventlet-0.22.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-enum34", when="@0.22:0.22.0")
        depends_on("py-greenlet@0.3:", when="@0.20:0.33")
