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

class Ravel(Package):
    """Ravel is a parallel communication trace visualization tool that
       orders events according to logical time."""

    homepage = "https://github.com/llnl/ravel"
    url = 'https://github.com/llnl/ravel/archive/v1.0.0.tar.gz'

    version('1.0.0', 'b25fece58331c2adfcce76c5036485c2')

    # TODO: make this a build dependency
    depends_on('cmake@2.8.9:')

    depends_on('muster@1.0.1:')
    depends_on('otf')
    depends_on('otf2')
    depends_on('qt@5:')

    def install(self, spec, prefix):
        cmake('-Wno-dev', *std_cmake_args)
        make()
        make("install")
