##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Cdhit(MakefilePackage):
    """CD-HIT is a very widely used program for clustering and comparing
       protein or nucleotide sequences."""

    homepage = "http://cd-hit.org/"
    url      = "https://github.com/weizhongli/cdhit/archive/V4.6.8.tar.gz"

    version('4.6.8', 'bdd73ec0cceab6653aab7b31b57c5a8b')

    variant('openmp', default=True, description='Compile with multi-threading support')

    depends_on('perl', type=('build', 'run'))

    def build(self, spec, prefix):
        mkdirp(prefix.bin)
        if '~openmp' in spec:
            make('openmp=no')
        else:
            make()

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PREFIX', prefix.bin)
