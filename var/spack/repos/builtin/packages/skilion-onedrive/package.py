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


class SkilionOnedrive(MakefilePackage):
    """A complete tool to interact with OneDrive on Linux,
    developed by Skilion, following the UNIX philosophy."""

    homepage = "https://github.com/skilion/onedrive"
    url      = "https://github.com/skilion/onedrive/archive/v1.1.1.tar.gz"

    version('1.1.1', sha256='fb51c81ec95c28f3fe3b29e3b7f915e30161bd5f4b14bb53ae5c2233cc1e92e9')

    depends_on('dmd')
    depends_on('curl')
    depends_on('sqlite')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        # Generate the version file
        makefile.filter('.git/HEAD .git/index', '', string=True)
        makefile.filter('$(shell git describe --tags)',
                        '{0}'.format(spec.version),
                        string=True)
        # Patch sqlite.d https://github.com/skilion/onedrive/issues/392
        sqlited = FileFilter('src/sqlite.d')
        sqlited.filter('std.c.stdlib', 'core.stdc.stdlib', String=True)

    def build(self, spec, prefix):
        make('onedrive', 'DESTDIR={0}'.format(prefix), 'PREFIX=/')

    def install(self, spec, prefix):
        make('install', 'DESTDIR={0}'.format(prefix), 'PREFIX=/')
