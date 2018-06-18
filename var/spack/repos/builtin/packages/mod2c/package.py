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


class Mod2c(CMakePackage):

    """MOD2C is NMODL to C converter adapted for CoreNEURON simulator.
    More information about NMODL can be found NEURON simulator
    documentation at Yale University."""

    homepage = "https://github.com/BlueBrain/mod2c"
    url      = "https://github.com/BlueBrain/mod2c.git"

    version('develop', git=url, preferred=True)

    depends_on('cmake@2.8.12:', type='build')

    def cmake_args(self):
        spec = self.spec
        options = []
        if 'bgq' in spec.architecture and '%xl' in spec:
            options.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return options

    def setup_environment(self, spack_env, run_env):
        run_env.set('MODLUNIT', join_path(self.prefix, 'share/nrnunits.lib'))
