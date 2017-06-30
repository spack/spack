##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Savanna(Package):
    """CODARcode Savanna runtime framework for high performance,
    workflow management using Swift/T and ADIOS.
    """

    homepage = "https://github.com/CODARcode/savanna"
    url = "https://github.com/CODARcode/savanna/archive/v0.5.tar.gz"

    version('develop', git='https://github.com/CODARcode/savanna.git',
            branch='master')
    version('0.5', '3f13adf29ec30f4acb2ba3fa07ed12b2')

    variant('tau', default=False, description='Enable TAU profiling support')

    depends_on('mpich')
    depends_on('stc')
    depends_on('adios@develop +staging')
    depends_on('mpix-launch-swift')
    depends_on('tau', when='+tau')

    def install(self, spec, prefix):
        make()
        install('README.md', prefix)
