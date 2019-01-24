# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExtutilsPkgconfig(PerlPackage):
    """simplistic interface to pkg-config"""

    homepage = "http://search.cpan.org/~xaoc/ExtUtils-PkgConfig-1.16/lib/ExtUtils/PkgConfig.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-PkgConfig-1.16.tar.gz"

    version('1.16', 'b86318f2b6ac6af3ee985299e1e38fe5')

    depends_on('pkgconfig', type=('build', 'run'))
