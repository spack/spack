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


class RNcdf4(RPackage):
    """Provides a high-level R interface to data files written using Unidata's
    netCDF library (version 4 or earlier), which are binary data files that are
    portable across platforms and include metadata information in addition to
    the data sets. Using this package, netCDF files (either version 4 or
    "classic" version 3) can be opened and data sets read in easily. It is also
    easy to create new netCDF dimensions, variables, and files, in either
    version 3 or 4 format, and manipulate existing netCDF files. This package
    replaces the former ncdf package, which only worked with netcdf version 3
    files. For various reasons the names of the functions have had to be
    changed from the names in the ncdf package. The old ncdf package is still
    available at the URL given below, if you need to have backward
    compatibility. It should be possible to have both the ncdf and ncdf4
    packages installed simultaneously without a problem. However, the ncdf
    package does not provide an interface for netcdf version 4 files."""

    homepage = "http://cirrus.ucsd.edu/~pierce/ncdf"
    url      = "https://cran.r-project.org/src/contrib/ncdf4_1.15.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ncdf4"

    version('1.15', 'cd60dadbae3be31371e1ed40ddeb420a')

    depends_on('netcdf')
