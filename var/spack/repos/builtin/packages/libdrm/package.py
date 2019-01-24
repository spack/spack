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
