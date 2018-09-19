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


class Bsseeker2(Package):
    """A versatile aligning pipeline for bisulfite sequencing data."""

    homepage = "http://pellegrini.mcdb.ucla.edu/BS_Seeker2"
    url      = "https://github.com/BSSeeker/BSseeker2/archive/v2.1.2.tar.gz"

    version('2.1.2',     '5f7f0ef4071711e56b59c5c16b7f34a7')

    depends_on('python@2.6:2.999', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('Antisense.py', prefix.bin)
        install_tree('bs_index', prefix.bin.bs_index)
        install('bs_seeker2-build.py', prefix.bin)
        install_tree('bs_utils', prefix.bin.bs_utils)
        install_tree('galaxy', prefix.bin.galaxy)
        install_tree('bs_align', prefix.bin.bs_align)
        install('bs_seeker2-align.py', prefix.bin)
        install('bs_seeker2-call_methylation.py', prefix.bin)
        install('FilterReads.py', prefix.bin)
