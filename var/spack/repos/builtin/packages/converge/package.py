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
from distutils.dir_util import copy_tree
import os


class Converge(Package):
    """CONVERGE is a revolutionary computational fluid dynamics (CFD) program
    that eliminates the grid generation bottleneck from the simulation process.
    CONVERGE was developed by engine simulation experts and is straightforward
    to use for both engine and non-engine simulations. Unlike many CFD
    programs, CONVERGE automatically generates a perfectly orthogonal,
    structured grid at runtime based on simple, user-defined grid control
    parameters. This grid generation method completely eliminates the need to
    manually generate a grid. In addition, CONVERGE offers many other features
    to expedite the setup process and to ensure that your simulations are as
    computationally efficient as possible."""

    homepage = "https://www.convergecfd.com/"
    url      = "https://download.convergecfd.com/download/CONVERGE_2.4/Full_Solver_Packages/converge_install_2.4.10.tar.gz"

    # In order to view available versions, you need to register for an account:
    # https://download.convergecfd.com/wp-login.php?action=register

    version('2.4.10', '53f5bd4bfb39005bebae46b8d6ee3ce6')
    version('2.3.16', '8b80f1e73a63181c427c7732ad279986')

    variant('mpi', default=True, description='Build with MPI support')

    # The CONVERGE Getting Started Guide recommends:
    #
    # +--------------+--------+---------+---------+
    # | MPI Packages |  v2.2  |  v2.3   |  v2.4   |
    # +--------------+--------+---------+---------+
    # | MPICH        | 1.2.1  | 3.1.4   |         |
    # | HP-MPI       | 2.0.3+ | 2.0.3+  |         |
    # | Platform MPI |        | 9.1.2   | 9.1.2   |
    # | Open MPI     | 1.6+   | 1.6+    | 1.10.1+ |
    # | Intel MPI    |        | 17.0.98 | 17.0.98 |
    # +--------------+--------+---------+---------+
    depends_on('mpi', when='+mpi')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['license/license.lic']
    license_vars = ['RLM_LICENSE']
    license_url = 'http://www.reprisesoftware.com/RLM_License_Administration.pdf'

    def install(self, spec, prefix):
        copy_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.set('CONVERGE_ROOT', self.prefix)
        run_env.prepend_path('PATH', join_path(self.prefix, 'l_x86_64', 'bin'))
