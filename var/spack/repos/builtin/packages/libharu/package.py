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


class Libharu(AutotoolsPackage):
    """libharu - free PDF library.

    Haru is a free, cross platform, open-sourced software library for
    generating PDF."""

    homepage = "http://libharu.org"
    url      = "https://github.com/libharu/libharu/archive/RELEASE_2_3_0.tar.gz"
    git      = "https://github.com/libharu/libharu.git"

    version('master', branch='master')
    version('2.3.0', '4f916aa49c3069b3a10850013c507460')
    version('2.2.0', 'b65a6fc33a0bdad89bec6b7def101f01')

    depends_on('libtool', type=('build'))
    depends_on('autoconf', type=('build'))
    depends_on('automake', type=('build'))
    depends_on('libpng')
    depends_on('zlib')

    def autoreconf(self, spec, prefix):
        """execute their autotools wrapper script"""
        if os.path.exists('./buildconf.sh'):
            bash = which('bash')
            bash('./buildconf.sh', '--force')

    def configure_args(self):
        """Point to spack-installed zlib and libpng"""
        spec = self.spec
        args = []

        args.append('--with-zlib={0}'.format(spec['zlib'].prefix))
        args.append('--with-png={0}'.format(spec['libpng'].prefix))

        return args

    def url_for_version(self, version):
        url = 'https://github.com/libharu/libharu/archive/RELEASE_{0}.tar.gz'
        return url.format(version.underscored)
