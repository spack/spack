##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "https://mesa.freedesktop.org/archive/13.0.6/mesa-13.0.6.tar.xz"
    list_url = "https://mesa.freedesktop.org/archive"
    list_depth = 2

    version('17.1.3', '1946a93d543bc219427e2bebe2ac4752')
    version('13.0.6', '1e5a769bc6cfd839cf3febcb179c27cc')
    version('12.0.6', '1a3d4fea0656c208db59289e4ed33b3f')
    version('12.0.3', '1113699c714042d8c4df4766be8c57d8')

    variant('swrender', default=False,
        description="Build with (gallium) software rendering.")

    variant('llvm', default=False,
        description="Use llvm for rendering pipes.")

    # General dependencies
    depends_on('python@2.6.4:')
    depends_on('py-mako@0.3.4:', type=('build', 'run'))
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')

    # Off-screen with llvmpipe
    # Note: there must be a better way of selecting the preferred llvm
    depends_on('llvm+link_dylib', when='+llvm')

    # For DRI and hardware acceleration
    depends_on('libpthread-stubs')
    depends_on('libdrm')
    depends_on('openssl')
    depends_on('libxcb@1.9.3:')
    depends_on('libxshmfence@1.1:', when='~swrender')
    depends_on('libx11', when='~swrender')
    depends_on('libxext', when='~swrender')
    depends_on('libxdamage', when='~swrender')
    depends_on('libxfixes')
    # depends_on('expat', when='~swrender')
    depends_on('libelf', when='+llvm~swrender')

    depends_on('glproto@1.4.14:', type='build', when='~swrender')
    depends_on('dri2proto@2.6:', type='build', when='~swrender')
    depends_on('dri3proto@1.0:', type='build', when='~swrender')
    depends_on('presentproto@1.0:', type='build', when='~swrender')

    # TODO: Add package for systemd, provides libudev
    # Using the system package manager to install systemd didn't work for me

    def configure_args(self):
        spec = self.spec
        args = []
        drivers = []
        if '+swrender' in spec:
            drivers = ['swrast']
            # Needs +llvm, but also C++14? -> drivers.append('swr')
            args.extend([
                '--disable-dri',
                '--disable-egl',
                '--disable-gbm',
                '--disable-gles1',
                '--disable-glx',
                '--disable-xvmc',
                '--enable-texture-float',
                '--enable-gallium-osmesa',
            ])

        if '+llvm' in spec:
            if self.spec.version < Version('17'):
                args.append('--enable-gallium-llvm')
            else:
                args.append('--enable-llvm')
            if '+link_dylib' in self.spec['llvm']:
                args.append('--enable-llvm-shared-libs')
            else:
                args.append('--disable-llvm-shared-libs')
            args.append('--with-llvm-prefix=%s' % spec['llvm'].prefix)

        if drivers:
            args.append('--with-gallium-drivers=' + ','.join(drivers))

        return args
