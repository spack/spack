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
import inspect


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "https://mesa.freedesktop.org/archive/12.0.3/mesa-12.0.3.tar.xz"
    list_url = "https://mesa.freedesktop.org/archive"
    list_depth = 2

    version('17.1.1', 'a4844bc6052578574f9629458bcbb749')
    version('13.0.6', '1e5a769bc6cfd839cf3febcb179c27cc')
    version('12.0.3', '1113699c714042d8c4df4766be8c57d8')

    variant('dri', default=False,
            description="Use DRI drivers for accelerated OpenGL rendering")
    variant('gallium', default=False,
            description="Build Gallium DRI drivers")

    # General dependencies
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')
    depends_on('binutils', type='build')
    depends_on('python@2.6.4:', type='build')
    depends_on('py-mako@0.3.4:', type='build')
    depends_on('gettext')
    depends_on('icu4c')
    depends_on('expat')
    depends_on('libpthread-stubs')
    depends_on('openssl')
    depends_on('xproto')
    depends_on('glproto@1.4.14:')
    depends_on('presentproto@1.0:')
    depends_on('libxcb@1.9.3:')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxshmfence@1.1:')
    depends_on('libxdamage')
    depends_on('libxfixes')
    depends_on('libxv')
    depends_on('libxvmc')

    # For DRI and hardware acceleration
    depends_on('libdrm', when='+dri')
    depends_on('dri2proto@2.6:', type='build', when='+dri')
    depends_on('dri3proto@1.0:', type='build', when='+dri')
    depends_on('llvm@3:3.99', when='+dri+gallium')

    # For optional features, possible new variants:
    #depends_on('libgcrypt')
    #depends_on('nettle')
    #depends_on('libelf')

    # TODO: Add package for systemd, provides libudev
    # Using the system package manager to install systemd didn't work for me

    def configure_args(self):
        spec = self.spec
        args = ['--enable-texture-float', '--enable-osmesa',
                '--enable-xa', '--enable-glx-tls']
        if '+dri' in spec:
            if 'llvm' in spec and '~link_dylib' in spec['llvm']:
                args.extend(['--disable-llvm-shared-libs'])
            if '~gallium' in spec:
                args.extend(['--without-gallium-drivers'])
        else:
            args.extend(['--disable-dri', '--disable-egl',
                         '--without-gallium-drivers'])
        return args

    def configure(self, spec, prefix):
        """Configure mesa, detecting if libsysfs is required
        for DRI support on the build host.
        """
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()
        configure = inspect.getmodule(self).configure

        with working_dir(self.build_directory, create=True):
            try:
                # First attempt uses libudev:
                configure(*options)
            except:
                if '+dri' in spec:
                    print('Configuring with libudev failed ... '
                          + ' trying libsysfs ...')
                    options.extend(['--enable-sysfs'])
                    configure(*options)
            else:
                raise
