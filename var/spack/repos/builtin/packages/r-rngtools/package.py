##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RRngtools(RPackage):
    """This package contains a set of functions for working with Random Number
    Generators (RNGs). In particular, it defines a generic S4 framework for
    getting/setting the current RNG, or RNG data that are embedded into objects
    for reproducibility. Notably, convenient default methods greatly facilitate
    the way current RNG settings can be changed."""

    homepage = "https://renozao.github.io/rngtools"
    url      = "https://cran.r-project.org/src/contrib/rngtools_1.2.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rngtools"

    version('1.2.4', '715967f8b3af2848a76593a7c718c1cd')

    depends_on('r-pkgmaker', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
