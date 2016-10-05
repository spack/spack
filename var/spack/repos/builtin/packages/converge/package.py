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
    computationally efficient as possible.

    Note: CONVERGE is licensed software. You will need to create an account on
    the CONVERGE homepage and download CONVERGE yourself. Spack will search
    your current directory for the download file. Alternatively, add this file
    to a mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.convergecfd.com/"
    url = "file://%s/converge_install_2.3.16.tar.gz" % os.getcwd()

    version('2.3.16', '8b80f1e73a63181c427c7732ad279986')

    variant('mpi', default=True, description='Build with MPI support')

    # The Converge Getting Started Guide recommends:
    # MPICH: 3.1.4
    # HP-MPI: 2.0.3+
    # OpenMPI: 1.6.*
    depends_on('mpi', when='+mpi')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['license/license.lic']
    license_vars = ['RLM_LICENSE']
    license_url = 'http://www.reprisesoftware.com/RLM_License_Administration.pdf'

    def install(self, spec, prefix):
        copy_tree('.', prefix)
