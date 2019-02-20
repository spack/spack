# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Usbmuxd(Package):
    """A socket daemon to multiplex connections from and to iOS devices."""

    homepage = "https://www.libimobiledevice.org/"
    url      = "https://www.libimobiledevice.org/downloads/usbmuxd-1.1.0.tar.bz2"
    git      = "https://git.libimobiledevice.org/usbmuxd.git"

    version('master', branch='master')
    version('1.1.0',  sha256='3e8948b4fe4250ee5c4bd41ccd1b83c09b8a6f5518a7d131a66fd38bd461b42d')

    depends_on('autoconf', when='@master')
    depends_on('automake', when='@master')
    depends_on('libtool',  when='@master')
    depends_on('libimobiledevice')
    depends_on('libplist')
    depends_on('libusb')
    depends_on('pkg-config')

    def install(self, spec, prefix):
        if self.spec.satisfies('@master'):
            autogen = Executable('./autogen.sh')
            autogen()
        configure('--disable-dependency-tracking',
                  '--disable-silent-rules',
                  '--prefix=%s' % self.spec.prefix)
        make('install')
