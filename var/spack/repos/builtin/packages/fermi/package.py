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


class Fermi(MakefilePackage):
    """A WGS de novo assembler based on the FMD-index for large genomes."""

    homepage = "https://github.com/lh3/fermi"
    url      = "https://github.com/downloads/lh3/fermi/fermi-1.1.tar.bz2"

    version('1.1', 'd5f006315652b6f18070b31474ca5ebb')

    depends_on('zlib')
    depends_on('perl', type='run')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('fermi', prefix.bin)
        install('run-fermi.pl', prefix.bin)
