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


class Raft(CMakePackage):
    """RAFT: Reconstruct Algorithms for Tomography.
       Toolbox under development at Brazilian Synchrotron Light Source."""

    homepage = "https://bitbucket.org/gill_martinez/raft_aps"
    url      = "https://bitbucket.org/gill_martinez/raft_aps/get/1.2.3.tar.gz"
    git      = "https://bitbucket.org/gill_martinez/raft_aps.git"

    version('develop', branch='master')
    version('1.2.3', '4d1b106d9b3493e63dde96f7dd44b834')

    depends_on('mpi')
    depends_on('cmake', type='build')
    depends_on('hdf5')
    depends_on('fftw')
    depends_on('cuda')

    def install(self, spec, prefix):
        """RAFT lacks an install in its CMakeList"""

        with working_dir(self.stage.source_path):
            mkdirp(prefix)

            # We only care about the binary
            install_tree('bin', prefix.bin)
