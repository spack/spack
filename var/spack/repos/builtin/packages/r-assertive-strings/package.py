# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveStrings(RPackage):
    """assertive.strings: Assertions to Check Properties of Strings"""

    homepage = "https://cloud.r-project.org/package=assertive.strings"
    url      = "https://cloud.r-project.org/src/contrib/assertive.strings_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.strings"

    version('0.0-3', sha256='d541d608a01640347d661cc9a67af8202904142031a20caa270f1c83d0ccd258')

    extends('r') 
    depends_on('r-assertive-base', type=('build', 'run'))
    depends_on('r-assertive-types', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
