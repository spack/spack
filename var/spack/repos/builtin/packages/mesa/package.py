##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
import distro


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "https://mesa.freedesktop.org/archive/12.0.3/mesa-12.0.3.tar.xz"

    list_url = "https://mesa.freedesktop.org/archive"

    version('17.1.1', 'a4844bc6052578574f9629458bcbb749')
    version('12.0.3', '1113699c714042d8c4df4766be8c57d8')

    variant('dri', default=True, description='Enable Hardware Acceleration')
    variant('osmesa', default=False, description='Enable Off Screen Rendering')
    variant('gdm', default=False, description='Enable GNOME Support')
    conflicts('+dri', '+osmesa')
    conflicts('~dri', '+osmesa')

    # General dependencies
    depends_on('python@2.6.4:')
    depends_on('py-mako@0.3.4:', type=('build', 'run'))
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')

    # For DRI and hardware acceleration
    depends_on('libpthread-stubs')
    depends_on('libdrm')
    depends_on('openssl')
    depends_on('libxcb@1.9.3:')
    depends_on('libxshmfence@1.1:')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxdamage')
    depends_on('libxfixes')

    depends_on('glproto@1.4.14:')
    depends_on('dri2proto@2.6:', when='+dri')
    depends_on('dri3proto@1.0:', when='+dri')
    depends_on('presentproto@1.0:')
    depends_on('pkg-config@0.9.0:')
    depends_on('llvm+link_dylib', when='+dri')
    depends_on('libdrm', when='+dri')

    def configure_args(self):
        spec = self.spec
        v = distro.linux_distribution()[1]
        distname = distro.linux_distribution()[0]

        # libudev too old on centos / rhel 6 so do sysfs
        if distname == "RedHatEnterpriseServer" or distname == "CentOS":
            if Version('6.0') <= Version(v) <= Version('6.999'):
                args = ['--enable-sysfs']
            else:
                args = []
        else:
            args = []

        # software rendering - works both v12 and v17
        if '~dri' in spec:
            args.extend([
                '--disable-dri',
                '--disable-egl',
                '--disable-driglx-direct',
                '--with-gallium-drivers=swrast',
            ])

        # hardware rendering - works v17
        elif '+dri' in spec:
            args.extend([
                '--enable-dri',
                '--enable-egl',
                '--enable-gles1',
                '--enable-gles2',
                '--enable-glx-tls',
                '--with-gallium-drivers=swrast'
            ])
        # off screen software rendering
        if '+osmesa' in spec:
            args.extend([
                '--enable-osmesa',
                '--disable-driglx-direct',
                '--disable-dri',
                '--with-gallium-drivers=swrast'
            ])
        if '+gdm' in spec:
            args.extend([
                '--enable-gdm'
            ])
        else:
            args.extend([
                '--disable-gdm'
            ])
        return args
