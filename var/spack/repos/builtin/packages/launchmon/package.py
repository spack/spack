# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Launchmon(AutotoolsPackage):
    """Software infrastructure that enables HPC run-time tools to
       co-locate tool daemons with a parallel job."""
    homepage = "https://github.com/LLNL/LaunchMON"
    url = "https://github.com/LLNL/LaunchMON/releases/download/v1.0.2/launchmon-v1.0.2.tar.gz"
    git      = "https://github.com/llnl/launchmon.git"

    version('master', branch='master')
    version('1.0.2', '8d6ba77a0ec2eff2fde2c5cc8fa7ff7a')

    depends_on('autoconf', type='build', when='@master')
    depends_on('automake', type='build', when='@master')
    depends_on('libtool', type='build', when='@master')
    depends_on('pkgconfig', type='build')
    depends_on('libgcrypt')
    depends_on('libgpg-error')
    depends_on("elf", type='link')
    depends_on("boost")
    depends_on("spectrum-mpi", when='arch=ppc64le')

    patch('launchmon-char-conv.patch', when='@1.0.2')

    def setup_environment(self, spack_env, run_env):
        if self.spec.satisfies('@master'):
            # automake for launchmon requires the AM_PATH_LIBGCRYPT macro
            # which is defined in libgcrypt.m4
            spack_env.prepend_path('ACLOCAL_PATH',
                                   self.spec['libgcrypt'].prefix.share.aclocal)
