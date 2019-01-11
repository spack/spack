# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFileSharedirInstall(PerlPackage):
    """Install shared files"""

    homepage = "http://search.cpan.org/~ether/File-ShareDir-Install-0.11/lib/File/ShareDir/Install.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/File-ShareDir-Install-0.11.tar.gz"

    version('0.11', '61107e6ce6eee42bf29525b1a4d029e0')

    depends_on('perl-module-build', type='build')
