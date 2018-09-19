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


class Hapcut2(MakefilePackage):
    """HapCUT2 is a maximum-likelihood-based tool for assembling haplotypes
       from DNA sequence reads, designed to 'just work' with excellent speed
       and accuracy."""

    homepage = "https://github.com/vibansal/HapCUT2"
    git      = "https://github.com/vibansal/HapCUT2.git"

    version('2017-07-10', commit='2966b94c2c2f97813b757d4999b7a6471df1160e',
            submodules=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('build'):
            install('extractFOSMID', prefix.bin)
            install('extractHAIRS', prefix.bin)
            install('HAPCUT2', prefix.bin)
