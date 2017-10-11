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


class RS4vectors(RPackage):
    """The S4Vectors package defines the Vector and List virtual classes and
       a set of generic functions that extend the semantic of ordinary
       vectors and lists in R. Package developers can easily implement
       vector-like or list-like objects as concrete subclasses of Vector or
       List. In addition, a few low-level concrete subclasses of general
       interest (e.g. DataFrame, Rle, and Hits) are implemented in the
       S4Vectors package itself (many more are implemented  in the IRanges
       package and in other Bioconductor infrastructure packages)."""

    homepage = "https://bioconductor.org/packages/S4Vectors/"
    url      = "https://bioconductor.org/packages/3.5/bioc/src/contrib/S4Vectors_0.14.4.tar.gz"
    list_url = homepage

    version('0.14.6', 'e40ba5de581fc54d70bd5c049415973c')
    version('0.14.4', '08ccc46e6d39f3aa9091f868ecec1f70')

    depends_on('r-biocgenerics', type=('build', 'run'))
