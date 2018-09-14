##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
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


class Flecsale(CMakePackage):
    """Flecsale is an ALE code based on FleCSI"""

    homepage = "https://github.com/laristra/flecsale"
    git      = "https://github.com/laristra/flecsale.git"

    version('develop', branch='master', submodules=True)

    variant('mpi', default=True,
            description='Build on top of mpi conduit for mpi inoperability')

    depends_on("cmake@3.1:", type='build')
    depends_on("flecsi~mpi", when='~mpi')
    depends_on("flecsi+mpi", when='+mpi')
    depends_on("python")
    depends_on("openssl")

    def cmake_args(self):
        options = [
            '-DENABLE_UNIT_TESTS=ON'
            '-DENABLE_OPENSSL=ON'
            '-DENABLE_PYTHON=ON'
        ]

        if '+mpi' in self.spec:
            options.extend([
                '-DENABLE_MPI=ON',
                '-DFLECSI_RUNTIME_MODEL=mpilegion'
            ])

        return options
