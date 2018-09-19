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


class Satsuma2(CMakePackage):
    """Satsuma2 is an optimsed version of Satsuma, a tool to reliably align
       large and complex DNA sequences providing maximum sensitivity (to find
       all there is to find), specificity (to only find real homology) and
       speed (to accomodate the billions of base pairs in vertebrate genomes).
    """

    homepage = "https://github.com/bioinfologics/satsuma2"
    git      = "https://github.com/bioinfologics/satsuma2.git"

    version('2016-11-22', commit='da694aeecf352e344b790bea4a7aaa529f5b69e6')

    def install(self, spec, prefix):
        install_tree(join_path('spack-build', 'bin'), prefix.bin)
