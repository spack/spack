# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libepoxy(AutotoolsPackage):
    """Epoxy is a library for handling OpenGL function pointer management for
    you."""
    homepage = "https://github.com/anholt/libepoxy"
    url      = "https://github.com/anholt/libepoxy/releases/download/1.4.3/libepoxy-1.4.3.tar.xz"
    list_url = "https://github.com/anholt/libepoxy/releases"

    version('1.5.5', sha256='261663db21bcc1cc232b07ea683252ee6992982276536924271535875f5b0556')
    version('1.5.4', sha256='0bd2cc681dfeffdef739cb29913f8c3caa47a88a451fd2bc6e606c02997289d2')
    version('1.5.3', sha256='002958c5528321edd53440235d3c44e71b5b1e09b9177e8daf677450b6c4433d')
    version('1.5.2', sha256='a9562386519eb3fd7f03209f279f697a8cba520d3c155d6e253c3e138beca7d8')
    version('1.5.1', sha256='ba25f9251bdd12fa11f06b4dbd29073dab6f120be9b941e91754c338b926c720')
    version('1.5.0', sha256='4c94995398a6ebf691600dda2e9685a0cac261414175c2adf4645cdfab42a5d5')
    version('1.4.3', sha256='0b808a06c9685a62fca34b680abb8bc7fb2fda074478e329b063c1f872b826f6')

    depends_on('pkgconfig', type='build')
    depends_on('gl')
    depends_on('libx11', when='+glx')

    variant('glx', default=True, description='enable GLX support')

    def configure_args(self):
        # Disable egl, otherwise configure fails with:
        # error: Package requirements (egl) were not met
        # Package 'egl', required by 'virtual:world', not found
        args = ['--enable-egl=no']

        # --enable-glx defaults to auto and was failing on PPC64LE systems
        # because libx11 was missing from the dependences. This explicitly
        # enables/disables glx support.
        if '+glx' in self.spec:
            args.append('--enable-glx=yes')
        else:
            args.append('--enable-glx=no')

        return args
