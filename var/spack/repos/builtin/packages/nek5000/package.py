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
import distutils.dir_util


class Nek5000(Package):
    """Nek5000 is an open source, highly scalable and portable spectral
       element code designed to simulate: unsteady Stokes, unsteady
       incompressible Navier-Stokes, low Mach-number flows, heat
       transfer and species transport incompressible
       magnetohydrodynamics (MHD).

       Since Nek5000 uses static arrays, there is no Nek5000 library,
       instead each application compiles directly the Nek5000 source code
       needed using  ${NEK_ROOT}/core/makenek. This an install of 
       Nek5000 is simply a copy of Nek5000
    """

    homepage = " https://nek5000.mcs.anl.gov"
    version('develop', git='https://github.com/Nek5000/Nek5000.git')
    version('0.0.0', git='https://github.com/Nek5000/Nek5000.git',
            commmit='315690e187ccc091c30fc46943f25e5714e2abd1')

    # TODO: determine how to get BLAS and MPI information to makenek
    depends_on('blas')
    depends_on('mpi')

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree('.', prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        #  users can locate makenek with thus; for example
        # ${NEK_ROOT}/core/makenek eddy_uv ${NEK_ROOT
        spack_env.set('NEK_ROOT', self.prefix)
