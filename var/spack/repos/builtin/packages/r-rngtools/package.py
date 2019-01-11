# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
