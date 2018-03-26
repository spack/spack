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


class Xmlf90(AutotoolsPackage):
    """xmlf90 is a suite of libraries to handle XML in Fortran."""

    homepage = "https://launchpad.net/xmlf90"
    url      = "https://launchpad.net/xmlf90/trunk/1.5/+download/xmlf90-1.5.2.tgz"

    version('1.5.2', '324fdcba7dafce83db26e72aab9f6656')

    depends_on('autoconf@2.69:', type='build')
    depends_on('automake@1.14:', type='build')
    depends_on('libtool@2.4.2:', type='build')
    depends_on('m4',             type='build')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('autogen.sh')

    def configure_args(self):
        if self.spec.satisfies('%gcc'):
            return ['FCFLAGS=-ffree-line-length-none']
        return []

    @run_after('install')
    def fix_mk(self):
        install(join_path(self.prefix, 'share', 'org.siesta-project',
                          'xmlf90.mk'), prefix)
