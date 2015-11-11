##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Scr(Package):
    """SCR caches checkpoint data in storage on the compute nodes of a
       Linux cluster to provide a fast, scalable checkpoint/restart
       capability for MPI codes"""

    homepage = "https://computation.llnl.gov/project/scr/"

    depends_on("mpi")
#    depends_on("dtcmp")

    version('1.1-7', 'a5930e9ab27d1b7049447c2fd7734ebd', url='http://downloads.sourceforge.net/project/scalablecr/releases/scr-1.1-7.tar.gz')
    version('1.1.8', '6a0f11ad18e27fcfc00a271ff587b06e', url='https://github.com/hpc/scr/releases/download/v1.1.8/scr-1.1.8.tar.gz')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--with-scr-config-file=" + prefix + "/etc/scr.conf")
        make()
        make("install")
