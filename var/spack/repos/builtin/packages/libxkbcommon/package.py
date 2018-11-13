# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxkbcommon(AutotoolsPackage):
    """xkbcommon is a library to handle keyboard descriptions, including
    loading them from disk, parsing them and handling their state. It's mainly
    meant for client toolkits, window systems, and other system
    applications."""

    homepage = "https://xkbcommon.org/"
    url      = "https://github.com/xkbcommon/libxkbcommon/archive/xkbcommon-0.8.0.tar.gz"

    version('0.8.0', '0d9738fb2ed2dcc6e2c6920d94e135ce')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('bison',    type='build')
    depends_on('xkbdata')

    def configure_args(self):
        spec = self.spec
        args = []
        args.append('--with-xkb-config-root={0}'
                    .format(spec['xkbdata'].prefix))
        return args
