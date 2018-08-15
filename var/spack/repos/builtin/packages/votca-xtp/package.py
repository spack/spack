##############################################################################
# Copyright (c) 2017-2018, The VOTCA Development Team (http://www.votca.org)
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
