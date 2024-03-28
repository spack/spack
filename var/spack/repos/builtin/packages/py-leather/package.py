# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLeather(PythonPackage):
    """Leather is the Python charting library for those who need charts now and
    don't care if they're perfect."""

    homepage = "https://leather.readthedocs.io/en/stable/"
    pypi = "leather/leather-0.3.3.tar.gz"

    license("MIT")

    version(
        "0.3.3",
        sha256="e0bb36a6d5f59fbf3c1a6e75e7c8bee29e67f06f5b48c0134407dde612eba5e2",
        url="https://pypi.org/packages/45/f4/692a53df6708caca1c6d088c6d9003940f164f98bd9df2bdc86233641e9c/leather-0.3.3-py3-none-any.whl",
    )
