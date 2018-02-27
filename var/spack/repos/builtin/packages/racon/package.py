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
import os
import shutil

class Racon(MakefilePackage):
    """Consensus module for raw de novo DNA assembly of long uncorrected
    reads.

    If you encounter build errors related to using the generated tar.gz file,
    try
    spack clean --all."""

    homepage = "https://github.com/isovic/racon"
    url      = "https://github.com/isovic/racon"

    version('master', git='git@github.com:isovic/racon.git',
            commit='0834442')

    depends_on('zlib')
    conflicts('%gcc@:4.8')

    parallel = False
    
    def edit(self, spec, prefix):
        return

    def build(self, spec, prefix):
        make('modules')
        make('tools')
        make()

    # from https://github.com/spack/spack/issues/31
    def install(self, spec, prefix):
        shutil.copytree('bin',os.path.join(prefix,'bin'),symlinks=True)
