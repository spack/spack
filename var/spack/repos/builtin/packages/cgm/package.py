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

class Cgm(Package):
    """The Common Geometry Module, Argonne (CGMA) is a code library
       which provides geometry functionality used for mesh generation and
       other applications."""
    homepage = "http://trac.mcs.anl.gov/projects/ITAPS/wiki/CGM"
    url      = "http://ftp.mcs.anl.gov/pub/fathom/cgm13.1.1.tar.gz"

    version('13.1.1', '4e8dbc4ba8f65767b29f985f7a23b01f')
    version('13.1.0', 'a6c7b22660f164ce893fb974f9cb2028')
    version('13.1'  , '95f724bda04919fc76818a5b7bc0b4ed')

    depends_on("mpi")

    def patch(self):
        filter_file('^(#include "CGMParallelConventions.h")',
                    '//\1',
                    'geom/parallel/CGMReadParallel.cpp')


    def install(self, spec, prefix):
        configure("--with-mpi",
                  "--prefix=%s" % prefix,
                  "CFLAGS=-static",
                  "CXXFLAGS=-static",
                  "FCFLAGS=-static")

        make()
        make("install")
