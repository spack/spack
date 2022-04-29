# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PerlFileSharedirInstall(PerlPackage):
    """Install shared files"""

    homepage = "https://metacpan.org/pod/File::ShareDir::Install"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/File-ShareDir-Install-0.11.tar.gz"

    version('0.11', sha256='32bf8772e9fea60866074b27ff31ab5bc3f88972d61915e84cbbb98455e00cc8')

    depends_on('perl-module-build', type='build')
