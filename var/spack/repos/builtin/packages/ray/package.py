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


class Ray(CMakePackage):
    """Parallel genome assemblies for parallel DNA sequencing"""

    homepage = "http://denovoassembler.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/denovoassembler/Ray-2.3.1.tar.bz2"

    version('2.3.1', '82f693c4db60af4328263c9279701009')

    depends_on('mpi')

    @run_after('build')
    def make(self):
        mkdirp(prefix.bin)
        make('PREFIX=%s' % prefix.bin)

    def install(self, spec, prefix):
        make('install')
