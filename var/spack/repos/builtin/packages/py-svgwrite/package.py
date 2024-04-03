# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySvgwrite(PythonPackage):
    """A Python library to create SVG drawings."""

    pypi = "svgwrite/svgwrite-1.1.12.zip"

    version(
        "1.1.12",
        sha256="4e84a0cd48bb116d26fa6f157e5902271bd1efb5ac5c6157d9811fda5a3d95a3",
        url="https://pypi.org/packages/9f/27/a29fc710b5fc4dc8031d55e903c1352a194df4014dccf8b507049dd754e6/svgwrite-1.1.12-py2.py3-none-any.whl",
    )
