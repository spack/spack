# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftobjectlibrary(CMakePackage):
    """FTObjectLibrary provides a collection of reference counted Fortran 2003
    classes to facilitate writing generic object oriented Fortran programs."""

    homepage = "https://github.com/trixi-framework/FTObjectLibrary"
    url = "https://github.com/trixi-framework/FTObjectLibrary"
    git = "https://github.com/trixi-framework/FTObjectLibrary.git"

    maintainers("schoonovernumerics")

    version("main", branch="main")
