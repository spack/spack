# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstropyIersData(PythonPackage):
    """IERS Earth rotation and leap second table

       Note: This package is not meant for standalone purposes
       but is needed by AstroPy"""

    homepage = "https://github.com/astropy/astropy-iers-data"
    git = "https://github.com/astropy/astropy-iers-data.git"

    maintainers("aweaver1fandm")
    
    version("main", branch="main", preferred=True)

    depends_on("python@3.8:")
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
