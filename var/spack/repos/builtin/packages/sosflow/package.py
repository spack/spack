# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
