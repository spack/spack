# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlUri(PerlPackage):
    """Uniform Resource Identifiers (absolute and relative)"""

    homepage = "http://search.cpan.org/~ether/URI-1.72/lib/URI.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/URI-1.72.tar.gz"

    version('1.74', sha256='a9c254f45f89cb1dd946b689dfe433095404532a4543bdaab0b71ce0fdcdd53d')
    version('1.73', sha256='cca7ab4a6f63f3ccaacae0f2e1337e8edf84137e73f18548ec7d659f23efe413')
    version('1.72', sha256='35f14431d4b300de4be1163b0b5332de2d7fbda4f05ff1ed198a8e9330d40a32')
    version('1.71', sha256='9c8eca0d7f39e74bbc14706293e653b699238eeb1a7690cc9c136fb8c2644115')

    depends_on('perl-test-needs', type=('build', 'test'))
