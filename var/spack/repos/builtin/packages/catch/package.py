##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Catch(Package):
    """Catch tests"""

    homepage = "https://github.com/philsquared/Catch"
    url = "https://github.com/philsquared/Catch/archive/v1.3.0.tar.gz"

    version('1.9.4', '110b9173d7f766487fed5b710836c7216a781568')
    version('1.9.3', 'dc0cd0b344d8ccb1190ac3447efcb49c9b43d497')
    version('1.9.2', '0580f57edd2b33ec671488dc7b6151f9e360c8c9')
    version('1.9.1', '10784fc4c3786dfc3bd222fb3f9b048b6d68f186')
    version('1.9.0', '62f07506d4a381d1730d494b71cff0396b9eb3d6')
    version('1.8.2', '45a7598a8e5c47bc09fb73eec205ffe0885983dc')
    version('1.8.1', 'd4e302f712fb7e75ce6f05b436dbaf21dca40030')
    version('1.8.0', '26064092b5682c9c997b04015ed1565f0e198827')
    version('1.7.2', '13018db2f0f0395456f695b0d0fbc490662e3467')
    version('1.7.1', 'f82e11a5cdfef2d36b5687ff5970d383f9e76490')
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
