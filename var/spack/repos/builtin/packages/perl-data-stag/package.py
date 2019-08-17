# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDataStag(PerlPackage):
    """Structured Tags datastructures"""

    homepage = "http://search.cpan.org/~cmungall/Data-Stag-0.14/Data/Stag.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CM/CMUNGALL/Data-Stag-0.14.tar.gz"

    version('0.14', 'f803acf74f1bfccc118aeac5483ee871')

    depends_on('perl-io-string', type=('build', 'run'))
