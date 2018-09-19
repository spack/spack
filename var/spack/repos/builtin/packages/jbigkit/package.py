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


class Jbigkit(MakefilePackage):
    """JBIG-Kit is a software implementation of
    the JBIG1 data compression standard."""

    homepage = "http://www.cl.cam.ac.uk/~mgk25/jbigkit/"
    url      = "http://www.cl.cam.ac.uk/~mgk25/jbigkit/download/jbigkit-2.1.tar.gz"

    version('2.1', 'ebcf09bed9f14d7fa188d3bd57349522')
    version('1.6', 'ce196e45f293d40ba76af3dc981ccfd7')

    build_directory = 'libjbig'

    def edit(self, spec, prefix):
        makefile = FileFilter('libjbig/Makefile')
        makefile.filter('CC = .*', 'CC = cc')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.include)
            for f in ['jbig85.h', 'jbig_ar.h', 'jbig.h']:
                install(f, prefix.include)
            mkdir(prefix.lib)
            for f in ['libjbig85.a', 'libjbig.a']:
                install(f, prefix.lib)
            mkdir(prefix.bin)
            for f in ['tstcodec', 'tstcodec85']:
                install(f, prefix.bin)
