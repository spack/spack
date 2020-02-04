# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Turbovnc(CMakePackage):
    """TurboVNC is a derivative of VNC (Virtual Network Computing)
    that is tuned to provide peak performance for 3D and video workloads.
    TurboVNC was originally a fork of TightVNC 1.3.x, on the surface,
    the X server and Windows viewer still behave similarly to their parents."""

    homepage = "http://www.turbovnc.org/"
    url      = "http://downloads.sourceforge.net/project/turbovnc/2.0.1/turbovnc-2.0.1.tar.gz"

    version('2.1.2', '9d04b26d40664d0d8072e8b1828f69c4')
    version('2.1.1', 'b1b1537eb5f8e6bd90acfd853277a9cf')
    version('2.1', '6748bb13647d318f0c932394f8298d10')
    version('2.0.1', 'a279fdb9ac86a1ebe82f85ab68353dcc')
    version('1.2.2', '556d97741199cf4e2f2d2b2fbee0069c')

    variant('java',    default=False, description='Enable Java build')
    variant('server',  default=True,  description='Enable server build')
    variant('x11deps', default=True,  description='Depends x11 depends')

    patch('x11deps.patch', when='@2.1:')

    depends_on("libx11", when='+x11deps')
    depends_on("libjpeg-turbo@1.3.1", when='@1.2.2')
    depends_on("libjpeg-turbo@1.5.1:", when='@2.1:')
    depends_on("libjpeg-turbo@1.5.1:+java", when='@2.1:+java',)
    depends_on('jdk', when='+java')
    depends_on('openssl', when='@2.2:')
    depends_on('openssl@:1.0.999', when='@:2.1')
    depends_on("pam", when='+server')
    depends_on("libxext", when='+x11deps')
    depends_on("libxdmcp", when='+x11deps')
    depends_on("libxau", when='+x11deps')
    depends_on("libxdamage", when='+x11deps')
    depends_on("libxcursor", when='+x11deps')
    depends_on("libxi", when='+java')
    depends_on("libxt", when='+java')
    depends_on("libxxf86vm", when='+x11deps')
    depends_on("libxxf86misc", when='+x11deps')
    depends_on("xf86vidmodeproto", when='+x11deps')
    # depends_on('libxkbfile')
    depends_on('xkeyboard-config+xorg', when='+x11deps', type=('build', 'run'))
    depends_on('font-util fonts=font-adobe-75dpi', when='+x11deps', type='run')
    depends_on('xkbcomp', when='+x11deps', type=('build', 'run'))
    depends_on('xauth', when='+x11deps', type=('build', 'run'))
    # depends_on('xkbdata', when='+x11deps', type='build')

    def cmake_args(self):

        options = []
        if '+java' in self.spec:
            options.append('-DTVNC_BUILDJAVA:BOOL=ON')
            options.append(
                '-DTJPEG_JAR:PATH=' + self.spec['libjpeg-turbo'].prefix +
                '/share/classes/turbojpeg.jar')
            options.append(
                '-DTJPEG_JNILIBRARY:PATH=' +
                self.spec['libjpeg-turbo'].prefix +
                '/lib/libturbojpeg.so')
        else:
            options.append('-DTVNC_BUILDJAVA:BOOL=OFF')
            options.append('-DTVNC_BUILDNATIVE:BOOL=ON')
        if '+server' in self.spec:
            options.append('-DTVNC_BUILDSERVER:BOOL=ON')
            if '~x11deps' in self.spec:
                options.append('-DTVNC_NVCONTROL:BOOL=ON')
        else:
            options.append('-DTVNC_BUILDSERVER:BOOL=OFF')
        if '+x11deps' in self.spec:
            options.append('-DXKB_BASE_DIRECTORY:PATH=' +
                           self.spec['xkeyboard-config'].prefix +
                           '/share/X11/xkb')
            options.append('-DXKB_BIN_DIRECTORY:PATH=' +
                           self.spec['xkbcomp'].prefix + '/bin')

        return options
