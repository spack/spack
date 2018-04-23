##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class ManDb(AutotoolsPackage):
    """man-db is an implementation of the standard Unix
    documentation system accessed using the man command. It uses
    a Berkeley DB database in place of the traditional
    flat-text whatis databases."""

    homepage = "http://www.nongnu.org/man-db/"
    url      = "http://git.savannah.nongnu.org/cgit/man-db.git/snapshot/man-db-2.7.6.1.tar.gz"

    version('2.7.6.1', '312761baade811db2b956af3432c285e')

    depends_on('autoconf')
    depends_on('automake')
    depends_on('gettext')
    depends_on('libpipeline')
    depends_on('flex')
    depends_on('groff', type=('build', 'link', 'run'))

    # TODO: add gzip support via a new package.
    # man pages are typically compressed, include all available
    # compression libraries
    depends_on('bzip2', type=('build', 'link', 'run'))
    depends_on('lzma',  type=('build', 'link', 'run'))
    depends_on('xz',    type=('build', 'link', 'run'))

    def configure_args(self):
        args = [
            '--disable-setuid',
            # defaults to a location that needs root privs to write in
            '--with-systemdtmpfilesdir={0}/tmp'.format(self.prefix)
        ]
        return args
