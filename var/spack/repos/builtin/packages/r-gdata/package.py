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


class RGdata(RPackage):
    """Various R programming tools for data manipulation, including: - medical
    unit conversions ('ConvertMedUnits', 'MedUnits'), - combining objects
    ('bindData', 'cbindX', 'combine', 'interleave'), - character vector
    operations ('centerText', 'startsWith', 'trim'), - factor manipulation
    ('levels', 'reorder.factor', 'mapLevels'), - obtaining information about R
    objects ('object.size', 'elem', 'env', 'humanReadable', 'is.what', 'll',
    'keep', 'ls.funs', 'Args','nPairs', 'nobs'), - manipulating MS-Excel
    formatted files ('read.xls', 'installXLSXsupport', 'sheetCount',
    'xlsFormats'), - generating fixed-width format files ('write.fwf'), -
    extricating components of date & time objects ('getYear', 'getMonth',
    'getDay', 'getHour', 'getMin', 'getSec'), - operations on columns of data
    frames ('matchcols', 'rename.vars'), - matrix operations ('unmatrix',
    'upperTriangle', 'lowerTriangle'), - operations on vectors ('case',
    'unknownToNA', 'duplicated2', 'trimSum'), - operations on data frames
    ('frameApply', 'wideByFactor'), - value of last evaluated expression
    ('ans'), and - wrapper for 'sample' that ensures consistent behavior for
    both scalar and vector arguments ('resample')."""

    homepage = "https://cran.r-project.org/package=gdata"
    url      = "https://cran.r-project.org/src/contrib/gdata_2.18.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gdata"

    version('2.18.0', 'f831019aa743fe11dcf0a051e4280921')
    version('2.17.0', 'c716b663b9dc16ad8cafe6acc781a75f')

    depends_on('r-gtools', type=('build', 'run'))
