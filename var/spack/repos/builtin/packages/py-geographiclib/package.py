# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeographiclib(PythonPackage):
    """The geodesic routines from GeographicLib."""

    homepage = "https://geographiclib.sourceforge.io/1.50/python"
    pypi = "geographiclib/geographiclib-1.50.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version(
        "1.50",
        sha256="51cfa698e7183792bce27d8fb63ac8e83689cd8170a730bf35e1a5c5bf8849b9",
        url="https://pypi.org/packages/8b/62/26ec95a98ba64299163199e95ad1b0e34ad3f4e176e221c40245f211e425/geographiclib-1.50-py3-none-any.whl",
    )
