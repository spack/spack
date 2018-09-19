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


class Glfmultiples(MakefilePackage):
    """glfMultiples is a GLF-based variant caller for next-generation
       sequencing data. It takes a set of GLF format genotype likelihood
       files as input and generates a VCF-format set of variant calls
       as output. """

    homepage = "https://genome.sph.umich.edu/wiki/GlfMultiples"
    url      = "http://www.sph.umich.edu/csg/abecasis/downloads/generic-glfMultiples-2010-06-16.tar.gz"

    version('2010-06-16', '64bf6bb7c76543f4c8fabce015a3cb11')

    depends_on('zlib')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('CXX=.*', 'CXX = ' + env['CXX'])
        makefile.filter('CFLAGS=.*',
                        'CFLAGS=-O2 -I./libsrc -I./pdf ' +
                        '-D_FILE_OFFSET_BITS=64 -D__USE_LONG_INT')

    def install(self, spec, prefix):
        make('INSTALLDIR=%s' % prefix, 'install')
