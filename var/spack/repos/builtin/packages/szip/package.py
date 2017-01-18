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


class Szip(AutotoolsPackage):
    """Szip is an implementation of the extended-Rice lossless
     compression algorithm.

    It provides lossless compression of scientific data, and is
    provided with HDF software products.
    """

    homepage = "https://www.hdfgroup.org/doc_resource/SZIP/"
    url = "http://www.hdfgroup.org/ftp/lib-external/szip/2.1/src/szip-2.1.tar.gz"

    version('2.1', '902f831bcefb69c6b635374424acbead')

    def configure_args(self):
        return ['--enable-production',
                '--enable-shared',
                '--enable-static',
                '--enable-encoding']
