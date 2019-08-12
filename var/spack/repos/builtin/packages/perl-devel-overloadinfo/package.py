# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDevelOverloadinfo(PerlPackage):
    """Returns information about overloaded operators for a given class"""

    homepage = "http://search.cpan.org/~ilmari/Devel-OverloadInfo-0.004/lib/Devel/OverloadInfo.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/I/IL/ILMARI/Devel-OverloadInfo-0.004.tar.gz"

    version('0.005', '607b65dfe9fdb47df780f3b22dcb7917')
    version('0.004', '97a27e31858b073daba54121d57be705')

    depends_on('perl-mro-compat', type=('build', 'run'))
