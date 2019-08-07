# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxpm(AutotoolsPackage):
    """libXpm - X Pixmap (XPM) image file format library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXpm"
    url      = "https://www.x.org/archive//individual/lib/libXpm-3.5.12.tar.gz"

    version('3.5.12', 'b286c884b11b5a0b4371175c5327141f')
    version('3.5.11', '7c67c878ee048206b070bc0b24154f04')
    version('3.5.10', 'a70507638d74541bf30a771f1e5938bb')
    version('3.5.9', 'd6d4b0f76248a6b346eb42dfcdaa72a6')
    version('3.5.8', '2d81d6633e67ac5562e2fbee126b2897')
    version('3.5.7', '7bbc8f112f7143ed6961a58ce4e14558')

    depends_on('gettext')
    depends_on('libx11')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def setup_environment(self, spack_env, run_env):
        # If libxpm is installed as an external package, gettext won't
        # be available in the spec. See
        # https://github.com/spack/spack/issues/9149 for details.
        if 'gettext' in self.spec:
            spack_env.append_flags('LDFLAGS', '-L{0} -lintl'.format(
                self.spec['gettext'].prefix.lib))
