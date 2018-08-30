##############################################################################
# Copyright (c) 2017-2018, The VOTCA Development Team (http://www.votca.org)
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


class VotcaTools(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the basic tools library of VOTCA.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/tools/tarball/v1.4"
    git      = "https://github.com/votca/tools.git"

    version('develop', branch='master')
    version('1.4', 'cd47868e9f28e2c7b9d01f95aa0185ca')
    version('1.4.1', '3176b72f8a41ec053cc740a5398e7dc4')

    depends_on("cmake@2.8:", type='build')
    depends_on("expat")
    depends_on("fftw")
    depends_on("gsl", when="@:1.4.9999")
    depends_on("eigen@3.3:", when="@1.5:")
    depends_on("boost")
    depends_on("sqlite")

    def cmake_args(self):
        args = [
            '-DWITH_RC_FILES=OFF'
        ]
        return args
