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
import os


class Nag(Package):
    """The NAG Fortran Compiler."""
    homepage = "http://www.nag.com/nagware/np.asp"

    version('6.1', 'f49bd548e0d5e2458b2dabb3ee01341a')
    version('6.0', '3fa1e7f7b51ef8a23e6c687cdcad9f96')

    # Licensing
    license_required = True
    license_comment = '!'
    license_files = ['lib/nag.key']
    license_vars = ['NAG_KUSARI_FILE']
    license_url = 'http://www.nag.com/doc/inun/np61/lin-mac/klicence.txt'

    def url_for_version(self, version):
        # TODO: url and checksum are architecture dependent
        # TODO: We currently only support x86_64
        url = 'http://www.nag.com/downloads/impl/npl6a{0}na_amd64.tgz'
        return url.format(version.joined)

    def install(self, spec, prefix):
        # Set installation directories
        os.environ['INSTALL_TO_BINDIR'] = prefix.bin
        os.environ['INSTALL_TO_LIBDIR'] = prefix.lib
        os.environ['INSTALL_TO_MANDIR'] = prefix + '/share/man/man'

        # Run install script
        os.system('./INSTALLU.sh')
