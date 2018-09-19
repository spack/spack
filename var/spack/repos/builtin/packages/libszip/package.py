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


class Libszip(AutotoolsPackage):
    """Szip is an implementation of the extended-Rice lossless
     compression algorithm.

    It provides lossless compression of scientific data, and is
    provided with HDF software products.
    """

    homepage = "https://support.hdfgroup.org/doc_resource/SZIP/"
    url      = "https://support.hdfgroup.org/ftp/lib-external/szip/2.1.1/src/szip-2.1.1.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/lib-external/szip"
    list_depth = 3

    provides('szip')

    version('2.1.1', '5addbf2a5b1bf928b92c47286e921f72')
    version('2.1',   '902f831bcefb69c6b635374424acbead')

    def configure_args(self):
        return [
            '--enable-production',
            '--enable-shared',
            '--enable-static',
            '--enable-encoding',
        ]
