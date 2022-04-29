# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class Vacuumms(CMakePackage):
    """VACUUMMS: (Void Analysis Codes and Unix Utilities for Molecular Modeling and
    Simulation) is a collection of research codes for the compuational analysis of
    free volume in molecular structures, including the generation of code for the
    production of high quality ray-traced images and videos."""

    homepage = "https://github.com/frankwillmore/VACUUMMS"
    url      = "https://github.com/frankwillmore/VACUUMMS/archive/refs/tags/v1.0.0.tar.gz"
    git      = "https://github.com/frankwillmore/VACUUMMS.git"

    maintainers = ['frankwillmore']

    version('master', branch='master')
    version('1.0.0', 'c18fe52f5041880da7f50d3808d37afb3e9c936a56f80f67838d045bf7af372f')

    depends_on('libtiff')
