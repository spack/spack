# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStatnetCommon(RPackage):
    """Non-statistical utilities used by the software developed by the
       Statnet Project. They may also be of use to others."""

    homepage = "http://www.statnet.org"
    url      = "https://cran.r-project.org/src/contrib/statnet.common_3.3.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/statnet.common"

    version('3.3.0', '36bc11098dcd3652a4beb05c156ad6c8')
