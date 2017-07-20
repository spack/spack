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


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    base_url = "ftp://ftp.freedesktop.org/pub/mesa/"
    url      = base_url + "12.0.3/mesa-12.0.3.tar.gz"

    version('13.0.2', 'cb828f9f68e0cd6c7ef30b9c67aa7cf2')
    version('13.0.1', '8415d4bb7837e6cfb0c819fdd19a643b')
    version('13.0.0', '7205edb90d0396dc26d049fa495f6fd1')
    version('12.0.3', '60c5f9897ddc38b46f8144c7366e84ad')

    variant('gallium', default=False, description="compile with gallium llvm sw rendering")
    variant('drm', default=True, description="compile with drm")

    # see http://www.paraview.org/Wiki/ParaView/ParaView_And_Mesa_3D
    conflicts('+gallium', when='@:9.2.2')

    # General dependencies
    depends_on('python@2.6.4:')
    depends_on('py-mako@0.3.4:', type=('build', 'run'))
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')

    # depends_on("llvm@3.0", when='@8.0.5~gallium')
    depends_on("libxml2+python", when='@8.0.5~gallium') 
    # depends_on("llvm+link_dylib+utils", when='@9:+gallium')
    # depends_on("llvm+shared_libs", when='@9:+gallium')
    depends_on('llvm@3.9.1', when='@13.0.2+gallium')

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
    depends_on('expat')

    depends_on('glproto@1.4.14:', type='build')
    depends_on('dri2proto@2.6:', type='build')
    depends_on('dri3proto@1.0:', type='build')
    depends_on('presentproto@1.0:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('binutils', type='build')

    # TODO: Add package for systemd, provides libudev
    # Using the system package manager to install systemd didn't work for me

    def url_for_version(self, version):
        """Handle mesa version-based custom URLs."""
        latest_mver = '11'

        if version < Version(latest_mver):
            base = Mesa.base_url + "/older-versions/%s.x" % (version.up_to(1))
        else:
            base = Mesa.base_url
        if version > Version('10.4'):
            name = 'mesa'
        else:
            name = 'MesaLib'
        return base + "/%s/%s-%s.tar.gz" % (version, name, version)

    def check_variants(self, var='', ver='', ref=''):
        if var and ver:
            error = "to be safe avoid '{variant}' with version '{version}' see:\n {reference}" # noqa
            if var in self.spec and self.spec.satisfies(ver):
                raise RuntimeError(
                    error.format(variant=var, version=ver, reference=ref))

    def configure_args(self):
        self.check_variants(
            var='+gallium',
            ver='@:9.2.2',
            ref='http://www.paraview.org/Wiki/ParaView/ParaView_And_Mesa_3D')
        args = []
        if '+gallium' in self.spec:
            args = ['--enable-opengl', '--disable-gles1', '--disable-gles2',
                    '--disable-va', '--disable-xvmc', '--disable-vdpa',
                    '--enable-gallium-llvm',
                    '--with-gallium-drivers=swrast,swr',
                    '--disable-dri', '--with-dri-drivers=',
                    '--disable-egl', '--with-egl-platforms=', '--disable-gb',
                    '--disable-osmesa', '--enable-gallium-osmesa']
            if '+shared_libs' in self.spec['llvm']:
                args.append('--enable-llvm-shared-libs')
            else:
                args.append('--disable-llvm-shared-libs')
            args.append('--with-llvm-prefix=' + self.spec['llvm'].prefix)
        return args

    def setup_environment(self, spack_env, run_env):
        if '+gallium' in self.spec:
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'lib'))
            run_env.set('GALLIUM_DRIVER', 'swr')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'lib'))
            run_env.set('GALLIUM_DRIVER', 'swr')
