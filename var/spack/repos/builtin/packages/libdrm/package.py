# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Libdrm(Package):
    """A userspace library for accessing the DRM, direct rendering manager,
    on Linux, BSD and other systems supporting the ioctl interface."""

    homepage = "http://dri.freedesktop.org/libdrm/"
    url      = "http://dri.freedesktop.org/libdrm/libdrm-2.4.59.tar.gz"

    version('2.4.99', sha256='597fb879e2f45193431a0d352d10cd79ef61a24ab31f44320168583e10cb6302')
    version('2.4.98', sha256='39789e2c37e7300324777a5c0a4ea1846537822b15ea3e630b0a000d8243ee97')
    version('2.4.97', sha256='8c6f4d0934f5e005cc61bc05a917463b0c867403de176499256965f6797092f1')
    version('2.4.96', sha256='d2bba5ca2ddfbdbc0f9f981835d31e1af373b9c1851014826c9698f80373c1bb')
    version('2.4.95', sha256='f0685d8b6ec173d964cd3a5bc98c5fcd89836505c42278863b78cebacae6f7e6')
    version('2.4.94', sha256='9b3d3509fe496839c4c52dfcfe6cc24f46f3dc272eab776ca6aa4d4a5c381597')
    version('2.4.93', sha256='bc67b2503106155c239c4e455b6718ef1b31675ea51f544c785c0e3295712861')
    version('2.4.92', sha256='a1b3b6430bc77697c689e572e32d58b3472c54300c9646c4ee8c626fc3bd62f1')
    version('2.4.91', sha256='c8ea3343d5bfc356550f0b5632403359d050fa09cf05d61e96e73adba0c407a9')
    version('2.4.90', sha256='750a3355fb6cdcee6dcfb366efbbe85d0efe4d9eb02c1f296d854470a1e12c99')
    version('2.4.89', sha256='c376b9ba0974700632939139397a12d4e3c93c31835a27dda855159441713e70')
    version('2.4.88', sha256='a8b458db6a73c717baee2e249d39511fb6f5c0f5f24dee2770935eddeda1a017')
    version('2.4.87', sha256='e813e2e8d7d9f071200317ee6b2ef6e35d4d497a57488ed3d44551e5970fc41a')
    version('2.4.86', sha256='90fca042dd5c619fff2771ab634c69010f25c582071519aa284860758fac2963')
    version('2.4.85', sha256='906aede5eb5a8b7860326324363e6d293d5af8f2c2de53d0922d1a7ab4f165a7')
    version('2.4.84', sha256='ca4d3a4705be2ec289f9df7cfa871f5e02fa43d0f653622c9d9d428959143e78')
    version('2.4.83', sha256='2ff5f626a14ec5bd680f7769cac9a8eb1e40c36cf5ca554d2c4e5d91bab3d81d')
    version('2.4.82', sha256='473997e1fa6f73f75f99bdeb8aa140f7efc3e774988b005c470343ee3cbeb97a')
    version('2.4.81', 'dc575dd661a082390e9f1366ca5734b0')
    version('2.4.75', '743c16109d91a2539dfc9cc56130d695')
    version('2.4.70', 'a8c275bce5f3d71a5ca25e8fb60df084')
    version('2.4.59', '105ac7af1afcd742d402ca7b4eb168b6')
    version('2.4.33', '86e4e3debe7087d5404461e0032231c8')

    depends_on('pkgconfig', type='build')
    depends_on('libpciaccess@0.10:', when=(sys.platform != 'darwin'))
    depends_on('libpthread-stubs')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix),
                  '--enable-static',
                  'LIBS=-lrt')  # This fixes a bug with `make check`

        make()
        make('check')
        make('install')
