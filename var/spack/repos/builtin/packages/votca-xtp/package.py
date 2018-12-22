# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaXtp(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA exciton transport engine.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/xtp/tarball/v1.4.1"
    git      = "https://github.com/votca/xtp.git"

    version('develop', branch='master')
    version('1.4.1', '31a2dbd8bd48bf337bc88b20ab312050')

    depends_on("cmake@2.8:", type='build')
    depends_on("votca-tools@develop", when='@develop')
    depends_on("votca-tools@1.4:1.4.999", when='@1.4:1.4.999')
    depends_on("votca-csg@develop", when='@develop')
    depends_on("votca-csg@1.4:1.4.999", when='@1.4:1.4.999')
    depends_on("votca-ctp@develop", when='@develop')
    depends_on("libxc", when='@1.5:')
    depends_on("ceres-solver", when='@1.5:')
