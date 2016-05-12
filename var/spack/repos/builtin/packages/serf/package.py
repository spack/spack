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

class Serf(Package):
    """Apache Serf - a high performance C-based HTTP client library built upon the Apache Portable Runtime (APR) library"""
    homepage  = 'https://serf.apache.org/'
    url       = 'https://archive.apache.org/dist/serf/serf-1.3.8.tar.bz2'

    version('1.3.8',     '1d45425ca324336ce2f4ae7d7b4cfbc5567c5446')

    depends_on('apr')
    depends_on('apr-util')
    depends_on('scons')
    depends_on('expat')
    depends_on('openssl')

    def install(self, spec, prefix):
        scons = which("scons")

        options = ['PREFIX=%s' % prefix]
        options.append('APR=%s' % spec['apr'].prefix)
        options.append('APU=%s' % spec['apr-util'].prefix)
        options.append('OPENSSL=%s' % spec['openssl'].prefix)
        options.append('LINKFLAGS=-L%s/lib' % spec['expat'].prefix)
        options.append('CPPFLAGS=-I%s/include' % spec['expat'].prefix)

        scons(*options)
        scons('install')
