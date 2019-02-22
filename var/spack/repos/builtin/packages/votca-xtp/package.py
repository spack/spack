# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('1.5', sha256='b40b6d19e13f0650e84b8beebe86ce5c09071624f18d66df826f9d8584b4d3c8')
    version('1.4.1', '31a2dbd8bd48bf337bc88b20ab312050')

    depends_on("cmake@2.8:", type='build')
    for v in ["1.4.1", "1.5", "develop"]:
        depends_on('votca-tools@%s' % v, when="@%s" % v)
        depends_on('votca-csg@%s' % v, when="@%s" % v)
    depends_on("votca-ctp@develop", when='@develop')
    depends_on("libxc", when='@1.5:')
    depends_on("ceres-solver", when='@1.5:')
