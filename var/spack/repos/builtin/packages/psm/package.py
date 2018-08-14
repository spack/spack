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


class Psm(MakefilePackage):
    """Intel Performance scaled messaging library"""

    homepage = "https://github.com/intel/psm"
    url      = "https://github.com/intel/psm/archive/v3.3.tar.gz"
    git      = "https://github.com/intel/psm.git"

    version('3.3', '031eb27688c932867d55054e76d00875', preferred=True)
    version('2017-04-28', commit='604758e')

    conflicts('%gcc@6:', when='@3.3')

    depends_on('libuuid')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('{DESTDIR}/usr/', '{LOCAL_PREFIX}/')

    def install(self, spec, prefix):
        make('LOCAL_PREFIX=%s' % prefix, 'install')
