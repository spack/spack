# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSplitstackshape(RPackage):
    """Stack and Reshape Datasets After Splitting Concatenated Values.

    Online data collection tools like Google Forms often export
    multiple-response questions with data concatenated in cells. The
    concat.split (cSplit) family of functions splits such data into
    separate cells. The package also includes functions to stack groups
    of columns and to reshape wide data, even when the data are
    "unbalanced" something which reshape (from base R) does not handle,
    and which melt and dcast from reshape2 do not easily handle.
    """

    homepage = "http://github.com/mrdwab/splitstackshape"
    url      = "https://cran.r-project.org/src/contrib/splitstackshape_1.4.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/splitstackshape"

    version('1.4.4', '54d2554fe92dfc4670a000b45baacc28')

    depends_on('r-data-table@1.9.4:', type=('build', 'run'))
    depends_on('r@2.10:', type=('build', 'run'))
