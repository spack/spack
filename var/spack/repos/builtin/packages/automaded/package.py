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


class Automaded(CMakePackage):
    """AutomaDeD (Automata-based Debugging for Dissimilar parallel
       tasks) is a tool for automatic diagnosis of performance and
       correctness problems in MPI applications. It creates
       control-flow models of each MPI process and, when a failure
       occurs, these models are leveraged to find the origin of
       problems automatically. MPI calls are intercepted (using
       wrappers) to create the models. When an MPI application hangs,
       AutomaDeD creates a progress-dependence graph that helps
       finding the process (or group of processes) that caused the hang.
    """

    homepage = "https://github.com/llnl/AutomaDeD"
    url      = "https://github.com/llnl/AutomaDeD/archive/v1.0.tar.gz"

    version('1.0', '16a3d4def2c4c77d0bc4b21de8b3ab03')

    depends_on('mpi')
    depends_on('boost')
    depends_on('callpath')
    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        return ['-DSTATE_TRACKER_WITH_CALLPATH=ON']
