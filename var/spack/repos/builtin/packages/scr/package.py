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

class Scr(CMakePackage):
    """SCR caches checkpoint data in storage on the compute nodes of a
       Linux cluster to provide a fast, scalable checkpoint/restart
       capability for MPI codes"""

    homepage = "http://computation.llnl.gov/projects/scalable-checkpoint-restart-for-mpi"

    ## NOTE: scr-v1.1.8 is built with autotools and is not properly build here.
    ## scr-v1.1.8 will be deprecated with the upcoming release of v1.2.0
    # url      = "https://github.com/LLNL/scr/releases/download/v1.1.8/scr-1.1.8.tar.gz"
    # version('1.1.8', '6a0f11ad18e27fcfc00a271ff587b06e')

    version('master', git='https://github.com/llnl/scr.git', branch='master')

    depends_on('pdsh')
    depends_on('zlib')
    depends_on('mpi')

    variant('dtcmp', default=True, description="DTCMP")
    depends_on('dtcmp', when="+dtcmp")

    ## YOGRT not yet in spack
    # variant('yogrt', default=True, description="Lib YOGRT")
    # depends_on('yogrt', when="+yogrt")

    ## MySQL not yet in spack
    # variant('mysql', default=True, decription="MySQL database for logging")
    # depends_on('mysql', when="+mysql")

    def cmake_args(self):
        args = []

        args.append('-DWITH_PDSH_PREFX={0}'.format(self.spec['pdsh'].prefix))

        if "+dtcmp" in self.spec:
                args.append('-DWITH_DTCMP_PREFIX={0}'.format(self.spec['dtcmp'].prefix))

        # if "+yogrt" in self.spec:
                # args.append('-DWITH_YOGRT_PREFIX={0}'.format(self.spec['yogrt'].prefix))

        # if "+mysql" in self.spec:
                # args.append('-DWITH_MYSQL_PREFIX={0}'.format(self.spec['mysql'].prefix))

        return args
