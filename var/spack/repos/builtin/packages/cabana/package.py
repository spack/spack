##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Cabana(CMakePackage):
    """The Exascale Co-Design Center for Particle Applications Toolkit
    """
    homepage = "https://github.com/ECP-copa/Cabana"
    git      = "https://github.com/ECP-copa/Cabana.git"
    url      = "https://github.com/ECP-copa/Cabana/archive/0.1.0.tar.gz"

    version('develop', branch='master', submodules=True)
    version('0.1.0-rc0', sha256='73754d38aaa0c2a1e012be6959787108fec142294774c23f70292f59c1bdc6c5')

    variant('serial', default=True, description="enable Serial backend (default)")
    variant('openmp', default=False, description="enable OpenMP backend")

    depends_on("cmake@3.9:", type='build')
    depends_on("kokkos+serial", when="+serial")
    depends_on("kokkos+openmp", when="+openmp")

    def cmake_args(self):
        options = [
            '-DCabana_ENABLE_TESTING=ON',
            '-DCabana_ENABLE_Serial=%s'  % (
                'On' if '+serial'  in self.spec else 'Off'),
            '-DCabana_ENABLE_OpenMP=%s'  % (
                'On' if '+openmp'  in self.spec else 'Off')
        ]

        return options
