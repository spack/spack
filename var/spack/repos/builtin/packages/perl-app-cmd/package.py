# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlAppCmd(PerlPackage):
    """Write command line apps with less suffering"""

    homepage = "http://search.cpan.org/~rjbs/App-Cmd/lib/App/Cmd.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/App-Cmd-0.331.tar.gz"

    version('0.331', 'b43c07d7b4d4e2a6baf32aa92cd00b93')
