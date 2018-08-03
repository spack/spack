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


class Diamond(CMakePackage):
    """DIAMOND is a sequence aligner for protein and translated DNA searches,
    designed for high performance analysis of big sequence data."""

    homepage = "https://ab.inf.uni-tuebingen.de/software/diamond"
    url      = "https://github.com/bbuchfink/diamond/archive/v0.9.14.tar.gz"

    version('0.9.21', '6f3c53520f3dad37dfa3183d61f21dd5')
    version('0.9.20', 'd73f4955909d16456d83b30d9c294b2b')
    version('0.9.19', '8565d2d3bfe407ee778eeabe7c6a7fde')
    version('0.9.14', 'b9e1d0bc57f07afa05dbfbb53c31aae2')
    version('0.8.38', 'd4719c8a7947ba9f743446ac95cfe644')
    version('0.8.26', '0d86305ab25cc9b3bb3564188d30fff2')

    depends_on('zlib')
