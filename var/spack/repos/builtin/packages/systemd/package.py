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


class Systemd(AutotoolsPackage):
    """systemd is a suite of basic building blocks for a Linux system.
    It provides a system and service manager that runs as PID 1 and starts
    the rest of the system."""

    homepage = "https://www.freedesktop.org/wiki/Software/systemd/"
    url      = "https://github.com/systemd/systemd/archive/v232.tar.gz"

    version('232', '3e3a0b14050eff62e68be72142181730')

    depends_on('glibc@2.16:')
    depends_on('libcap')
    depends_on('util-linux@2.27.1:')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('autoconf',          type='build')
    depends_on('automake',          type='build')
    depends_on('libtool',           type='build')
    depends_on('m4',                type='build')
    depends_on('intltool@0.40.0:',  type='build')
    depends_on('gettext',           type='build')
    depends_on('coreutils',         type='build')
    depends_on('python',            type='build')

    # requires XML::Parser perl module
    # depends_on('perl@5.8.1:', type='build')

    def autoreconf(self, spec, prefix):
        libtoolize()
        intltoolize('--force', '--automake')
        autoreconf(
            '--force', '--install', '--symlink',
            '-I', join_path(spec['pkg-config'].prefix, 'share', 'aclocal'),
            '-I', join_path(spec['gettext'].prefix, 'share', 'aclocal')
        )
