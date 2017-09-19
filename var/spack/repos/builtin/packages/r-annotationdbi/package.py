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
#
#
from spack import *


class RAnnotationdbi(RPackage):
    """Provides user interface and database connection code for 
annotation data packages using SQLite data storage."""

    homepage = "https://www.bioconductor.org/packages/AnnotationDbi/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/AnnotationDbi_1.38.2.tar.gz"
    list_url = homepage
    version('1.38.2', 'aea4a5cd1f752b59cb9f4a8dcca05734')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))


