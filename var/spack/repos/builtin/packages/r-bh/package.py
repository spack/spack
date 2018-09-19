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


class RBh(RPackage):
    """Boost provides free peer-reviewed portable C++ source libraries. A large
    part of Boost is provided as C++ template code which is resolved entirely
    at compile-time without linking. This package aims to provide the most
    useful subset of Boost libraries for template use among CRAN package. By
    placing these libraries in this package, we offer a more efficient
    distribution system for CRAN as replication of this code in the sources of
    other packages is avoided. As of release 1.60.0-2, the following Boost
    libraries are included: 'algorithm' 'any' 'bimap' 'bind' 'circular_buffer'
    'concept' 'config' 'container' 'date'_'time' 'detail' 'dynamic_bitset'
    'exception' 'filesystem' 'flyweight' 'foreach' 'functional' 'fusion'
    'geometry' 'graph' 'heap' 'icl' 'integer' 'interprocess' 'intrusive' 'io'
    'iostreams' 'iterator' 'math' 'move' 'mpl' 'multiprcecision' 'numeric'
    'pending' 'phoenix' 'preprocessor' 'random' 'range' 'smart_ptr' 'spirit'
    'tuple' 'type_trains' 'typeof' 'unordered' 'utility' 'uuid'."""

    homepage = "https://cran.r-project.org/web/packages/BH/index.html"
    url      = "https://cran.r-project.org/src/contrib/BH_1.65.0-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/BH"
    version('1.65.0-1', '7d0402188e4af59f4103f36616d6ee55')
    version('1.60.0-2', 'b50fdc85285da05add4e9da664a2d551')
