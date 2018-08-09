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


class Sosflow(CMakePackage):
    """SOSflow provides a flexible, scalable, and programmable framework for
    observation, introspection, feedback, and control of HPC applications."""

    homepage = "https://github.com/cdwdirect/sos_flow/wiki"
    git      = "https://github.com/cdwdirect/sos_flow.git"

    version('spack', tag='spack-build-v0.9901')

    depends_on('libevpath')
    depends_on('sqlite@3:')
    depends_on('pkgconfig')
    depends_on('mpi')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('SOS_HOST_KNOWN_AS', 'SPACK-SOS-BUILD')
        spack_env.set('SOS_HOST_NODE_NAME', 'SPACK-SOS-NODE')
        spack_env.set('SOS_HOST_DETAILED', 'SPACK-SOS-DETAILED')

        run_env.set('SOS_ROOT', self.spec.prefix)
        run_env.set('SOS_BUILD_DIR', self.spec.prefix)
        run_env.set('SOS_CMD_PORT', '22500')
        run_env.set('SOS_WORK', env['HOME'])
        run_env.set('SOS_EVPATH_MEETUP', env['HOME'])
        run_env.set('SOS_ENV_SET', 'true')
