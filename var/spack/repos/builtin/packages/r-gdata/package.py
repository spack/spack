# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    homepage = "https://cloud.r-project.org/package=gdata"
    url      = "https://cloud.r-project.org/src/contrib/gdata_2.18.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gdata"

    version('2.18.0', 'f831019aa743fe11dcf0a051e4280921')
    version('2.17.0', 'c716b663b9dc16ad8cafe6acc781a75f')

    depends_on('r@2.3.0:', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('perl@5.10.0:')
