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


class Seqtk(Package):
    """Toolkit for processing sequences in FASTA/Q formats."""

    homepage = "https://github.com/lh3/seqtk"
    url      = "https://github.com/lh3/seqtk/archive/v1.1.tar.gz"

    version('1.2', '255ffe05bf2f073dc57abcff97f11a37')
    version('1.1', 'ebf5cc57698a217150c2250494e039a2')

    depends_on('zlib')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install('seqtk', prefix.bin)
        set_executable(join_path(prefix.bin, 'seqtk'))
