##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Catch(Package):
    """Catch tests"""

    homepage = "https://github.com/philsquared/Catch"
    url = "https://github.com/philsquared/Catch/archive/v1.3.0.tar.gz"

    version('1.7.0', 'fe39f5b3eb07a5dd0e3f84a1335ceca7de8982e6')
    version('1.6.1', '7d46961a3131655b986123f8a1f439a04a0af623')
    version('1.6.0', '890a3b21085d796e13c3bfaf4b6c6f1d06e4a52e')
    version('1.5.9', '8bc32146a5a2789cd3d3ce2893772e32f412f1b1')
    version('1.5.0', 'c87397846ea5126febd39f513b413e32f9ed552b')
    version('1.4.0', 'c165406968fbfb46949885da571cd528c62c4d9a')
    version('1.3.5', '31553ba6e4bd0cc61e0507d6754847e354699284')
    version('1.3.0', 'e13694aaff72817d02af8ed27d077cd261b6e857')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install(join_path('single_include', 'catch.hpp'), prefix.include)
        # fakes out spack so it installs a module file
        mkdirp(join_path(prefix, 'bin'))
