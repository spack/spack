# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFileCopyRecursive(PerlPackage):
    """Perl extension for recursively copying files and directories"""

    homepage = "http://search.cpan.org/~dmuey/File-Copy-Recursive-0.38/Recursive.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DM/DMUEY/File-Copy-Recursive-0.38.tar.gz"

    version('0.40', '659c634f248885c4b3876b15baf56c79')
    version('0.38', 'e76dc75ab456510d67c6c3a95183f72f')
