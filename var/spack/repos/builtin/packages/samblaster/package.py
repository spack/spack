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


class Samblaster(MakefilePackage):
    """A tool to mark duplicates and extract discordant and split reads from
    sam files."""

    homepage = "https://github.com/GregoryFaust/samblaster"
    url      = "https://github.com/GregoryFaust/samblaster/archive/v.0.1.24.tar.gz"

    version('0.1.24', '885d5782cc277865dfb086fc0a20243e')
    version('0.1.23', '95d33b6fcceaa38a9bd79014446b4545')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('samblaster', prefix.bin)
