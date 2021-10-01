# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Mpibind(AutotoolsPackage):
    """A memory-driven algorithm to map parallel codes
    to heterogeneous architectures"""

    homepage    = "https://github.com/LLNL/mpibind"
    url         = "https://github.com/LLNL/mpibind/archive/refs/tags/v0.5.0.tar.gz"
    git         = "https://github.com/LLNL/mpibind.git"

    maintainers = ['eleon']

    # The build process uses 'git describe --tags' to get the
    # package version, thus we need 'get_full_repo'
    version('master', branch='master', get_full_repo=True)
    version('0.7.0', sha256='33077e7eb50322d2bcfe87bb3ea9159c2e49f6f045cbbcd2e69e763c3bec4330')
    version('0.5.0', sha256='51bb27341109aeef121a8630bd56f5551c70ebfd337a459fb70ef9015d97d2b7')

    variant('cuda', default=False,
            description='Build w/support for NVIDIA GPUs.')
    variant('rocm', default=False,
            description='Build w/support for AMD GPUs.')
    variant('flux', default=False,
            description='Build the Flux plugin.')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('pkgconf',  type='build')

    depends_on('hwloc@2:+libxml2', type='link')
    depends_on('hwloc@2:+pci', when=(sys.platform != 'darwin'), type='link')
    depends_on('hwloc@2:+cuda+nvml', when='+cuda', type='link')
    depends_on('hwloc@2.4:+rocm+opencl', when='+rocm', type='link')

    # Requiring @master temporarily while Flux adds
    # FLUX_SHELL_RC_PATH to a stable version (>0.29.0).
    # mpibind will require at least such version.
    depends_on('flux-core@master', when='+flux', type='link')

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')

    @when('+flux')
    def setup_run_environment(self, env):
        """Load the mpibind plugin into Flux"""
        env.prepend_path('FLUX_SHELL_RC_PATH',
                         join_path(self.prefix, 'share', 'mpibind'))

    # To build and run the tests, make sure 'libtap' is installed
    # on the target system and is recognized by pkg-config.
    # Unfortunately, libtap is not in Spack.
