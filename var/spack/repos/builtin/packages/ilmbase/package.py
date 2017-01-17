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


class Ilmbase(AutotoolsPackage):
    """OpenEXR ILM Base libraries (high dynamic-range image file format)"""

    homepage = "http://www.openexr.com/"
    url      = "http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.2.0.tar.gz"

    version('2.2.0', 'b540db502c5fa42078249f43d18a4652')
    version('2.1.0', 'af1115f4d759c574ce84efcde9845d29')
    version('2.0.1', '74c0d0d2873960bd0dc1993f8e03f0ae')
    version('1.0.2', '26c133ee8ca48e1196fbfb3ffe292ab4')
    version('0.9.0', '4df45f8116cb7a013b286caf6da30a2e')
