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


class RJsonlite(RPackage):
    """A fast JSON parser and generator optimized for statistical data and the
    web. Started out as a fork of 'RJSONIO', but has been completely rewritten
    in recent versions. The package offers flexible, robust, high performance
    tools for working with JSON in R and is particularly powerful for building
    pipelines and interacting with a web API. The implementation is based on
    the mapping described in the vignette (Ooms, 2014). In addition to
    converting JSON data from/to R objects, 'jsonlite' contains functions to
    stream, validate, and prettify JSON data. The unit tests included with the
    package verify that all edge cases are encoded and decoded consistently for
    use with dynamic data in systems and applications."""

    homepage = "https://github.com/jeroenooms/jsonlite"
    url      = "https://cran.r-project.org/src/contrib/jsonlite_1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/jsonlite"

    version('1.2', '80cd2678ae77254be470f5931db71c51')
    version('1.0', 'c8524e086de22ab39b8ac8000220cc87')
    version('0.9.21', '4fc382747f88a79ff0718a0d06bed45d')
