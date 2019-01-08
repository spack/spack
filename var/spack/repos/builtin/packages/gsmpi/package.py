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


class Gsmpi(CMakePackage):
    """GS-MPI encapsulates the gather-scatter exchange routines
    and parallel direct solver from Nek5000 (http://nek5000.mcs.anl.gov/)."""

    homepage = "https://gitlab.nektar.info/archive/nektar/tree/5fdc271a53d91d97dc9d13695ec8bc1f4b7a390b/ThirdParty/gsmpi-1.2"
    url      = "http://www.nektar.info/thirdparty/gsmpi-1.2.tar.bz2"

    version('1.2.1_1', sha256='c9bc966c92f45e81f4e9d1887dd7c59808e7a4ef9ec41e1e5f1e6c5c01745211')
    version('1.2.1',   sha256='c9d51109ec342ae93e9892821278d0d3c20d0559bbd4218e04ea27b911ce61a2')

    depends_on('mpi')
    depends_on('cmake@:3.4.99')

    @run_after('install')
    def install_headers(self):
        return
