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


class Mpibash(AutotoolsPackage):
    """Parallel scripting right from the Bourne-Again Shell (Bash)"""

    homepage = "https://github.com/lanl/MPI-Bash"
    url      = "https://github.com/lanl/MPI-Bash/releases/download/v1.2/mpibash-1.2.tar.gz"

    version('1.2', 'b81001fb234ed79c4e5bf2f7efee3529')

    depends_on('bash@4.4:')
    # uses MPI_Exscan which is in MPI-1.2 and later
    depends_on('mpi@1.2:')

    depends_on('libcircle')

    def configure_args(self):
        args = [
            "--with-bashdir={0}".format(self.spec['bash'].prefix.include.bash),
            "CC={0}".format(self.spec['mpi'].mpicc)
        ]
        return args
