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


class Icet(CMakePackage):
    """The Image Composition Engine for Tiles (IceT) is a high-performance
       sort-last parallel rendering library."""

    homepage = "http://icet.sandia.gov"
    url = "https://example.com/icet-1.2.3.tar.gz"

    version('develop', branch='master',
            git='https://gitlab.kitware.com/icet/icet.git')
    version('2.1.1', '4f971c51105a64937460d482adca2a6c')

    depends_on('mpi')

    def url_for_version(self, version):
        return ("https://gitlab.kitware.com/icet/icet/repository/"
                "archive.tar.bz2?ref=IceT-{0}".format(version.dotted))

    def cmake_args(self):
        return ['-DICET_USE_OPENGL:BOOL=OFF']
