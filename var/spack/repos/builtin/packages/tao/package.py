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


class Tao(Package):
    """The Toolkit for Advanced Optimization (TAO) is aimed at the solution of
    large-scale optimization problems on high-performance architectures.

    As of PETSc version 3.5, TAO is now included as part of the PETSc
    distribution. This package is deprecated."""

    homepage = "http://www.mcs.anl.gov/research/projects/tao/tao-deprecated/index.html"
    url      = "http://www.mcs.anl.gov/research/projects/tao/tao-deprecated/download/tao-2.2.2.tar.gz"

    version('2.2.2', 'c3eaaa192cc1f70b0fd8e5285973e515')

    depends_on('petsc@3.4.0:3.4.999~complex', when='@2.2.2')

    def install(self, spec, prefix):
        make('all')

    def setup_environment(self, spack_env, run_env):
        # configure fails if these env vars are set outside of Spack
        spack_env.unset('TAO_DIR')
        spack_env.unset('TAO_ARCH')

        # Set TAO_DIR in the module file
        run_env.set('TAO_DIR', self.prefix)
        run_env.unset('TAO_ARCH')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Set up TAO_DIR for everyone using PETSc package
        spack_env.set('TAO_DIR', self.prefix)
        spack_env.unset('TAO_ARCH')
