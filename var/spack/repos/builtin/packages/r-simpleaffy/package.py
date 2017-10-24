##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RSimpleaffy(RPackage):
    """Provides high level functions for reading Affy .CEL files,
       phenotypic data, and then computing simple things with it, such as
       t-tests, fold changes and the like. Makes heavy use of the affy
       library. Also has some basic scatter plot functions and mechanisms
       for generating high resolution journal figures..."""

    homepage = "http://bioconductor.org/packages/simpleaffy/"
    url      = "https://bioconductor.org/packages/3.5/bioc/src/contrib/simpleaffy_2.52.0.tar.gz"

    version('2.52.0', 'aa305099a57b3d868be53dc8c539b74e')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.52.0')
