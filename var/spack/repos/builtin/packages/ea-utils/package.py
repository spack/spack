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


class EaUtils(MakefilePackage):
    """Command-line tools for processing biological sequencing data. Barcode
       demultiplexing, adapter trimming, etc. Primarily written to support an
       Illumina based pipeline - but should work with any FASTQs."""

    homepage = "http://expressionanalysis.github.io/ea-utils/"
    url = "https://github.com/ExpressionAnalysis/ea-utils/archive/1.04.807.tar.gz"

    version('1.04.807', '5972b9f712920603b7527f46c0063a09')

    depends_on('subversion')
    depends_on('zlib')
    depends_on('gsl')
    depends_on('bamtools')
    # perl module required for make check, which is included in the default
    # target
    depends_on('perl', type='build')

    build_directory = 'clipper'

    def edit(self, spec, prefix):
        with working_dir('clipper'):
            makefile = FileFilter('Makefile')
            makefile.filter('/usr', prefix)
