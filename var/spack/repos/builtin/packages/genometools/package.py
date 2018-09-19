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
#############################################################################
from spack import *


class Genometools(MakefilePackage):
    """genometools is a free collection of bioinformatics tools (in the realm
       of genome informatics) combined into a single binary named gt."""

    homepage = "http://genometools.org/"
    url      = "http://genometools.org/pub/genometools-1.5.9.tar.gz"

    version('1.5.9', 'e400d69092f9f13db09b33f9dea39d2e')

    depends_on('perl', type=('build', 'run'))
    depends_on('cairo')
    depends_on('pango')

    # build fails with gcc 7"
    conflicts('%gcc@7.1.0:')

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('CPATH', self.prefix.include.genometools)
