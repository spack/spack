# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaCtp(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA charge transport engine.
    """
    homepage = "http://www.votca.org"
    git      = "https://github.com/votca/ctp.git"

    version('develop', branch='master')

    depends_on("cmake@2.8:", type='build')
    depends_on("votca-tools@develop", when='@develop')
    depends_on("votca-csg@develop", when='@develop')
    depends_on("gsl")
