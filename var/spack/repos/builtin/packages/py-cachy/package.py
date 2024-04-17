# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachy(PythonPackage):
    """Cachy provides a simple yet effective caching library."""

    homepage = "https://github.com/sdispater/cachy"
    pypi = "cachy/cachy-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.3.0",
        sha256="338ca09c8860e76b275aff52374330efedc4d5a5e45dc1c5b539c1ead0786fe7",
        url="https://pypi.org/packages/82/e6/badd9af6feee43e76c3445b2621a60d3d99fe0e33fffa8df43590212ea63/cachy-0.3.0-py2.py3-none-any.whl",
    )
