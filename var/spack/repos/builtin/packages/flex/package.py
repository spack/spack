##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import os


class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""

    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/releases/download/v2.6.1/flex-2.6.1.tar.gz"

    version('2.6.4', '2882e3179748cc9f9c23ec593d6adc8d')
    # 2.6.4 fails to compile with gcc@7.2:
    # see https://github.com/spack/spack/issues/8152 and
    # https://github.com/spack/spack/issues/6942
    version('2.6.3', 'a5f65570cd9107ec8a8ec88f17b31bb1', preferred=True)
    # Avoid flex '2.6.2' (major bug)
    # See issue #2554; https://github.com/westes/flex/issues/113
    version('2.6.1', '05bcd8fb629e0ae130311e8a6106fa82')
    version('2.6.0', '760be2ee9433e822b6eb65318311c19d')
    version('2.5.39', '5865e76ac69c05699f476515592750d7')

    variant('lex', default=True,
            description="Provide symlinks for lex and libl")

    depends_on('bison',         type='build')
    depends_on('gettext@0.19:', type='build')
    depends_on('help2man',      type='build')

    # Older tarballs don't come with a configure script
    depends_on('m4',       type='build')
    depends_on('autoconf', type='build', when='@:2.6.0')
    depends_on('automake', type='build', when='@:2.6.0')
    depends_on('libtool',  type='build', when='@:2.6.0')

    # Build issue for v2.6.4 when gcc@7.2.0: is used
    # See issue #219; https://github.com/westes/flex/issues/219
    conflicts('%gcc@7.2.0:', when='@2.6.4')

    def url_for_version(self, version):
        url = "https://github.com/westes/flex"
        if version >= Version('2.6.1'):
            url += "/releases/download/v{0}/flex-{0}.tar.gz".format(version)
        elif version == Version('2.6.0'):
            url += "/archive/v{0}.tar.gz".format(version)
        elif version >= Version('2.5.37'):
            url += "/archive/flex-{0}.tar.gz".format(version)
        else:
            url += "/archive/flex-{0}.tar.gz".format(version.dashed)

        return url

    @run_after('install')
    def symlink_lex(self):
        """Install symlinks for lex compatibility."""
        if self.spec.satisfies('+lex'):
            dso = dso_suffix
            for dir, flex, lex in \
                    ((self.prefix.bin,   'flex', 'lex'),
                     (self.prefix.lib,   'libfl.a', 'libl.a'),
                     (self.prefix.lib,   'libfl.' + dso, 'libl.' + dso),
                     (self.prefix.lib64, 'libfl.a', 'libl.a'),
                     (self.prefix.lib64, 'libfl.' + dso, 'libl.' + dso)):

                if os.path.isdir(dir):
                    with working_dir(dir):
                        if (os.path.isfile(flex) and not os.path.lexists(lex)):
                            symlink(flex, lex)
