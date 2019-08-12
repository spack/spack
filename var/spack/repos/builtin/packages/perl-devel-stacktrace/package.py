# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDevelStacktrace(PerlPackage):
    """An object representing a stack trace."""

    homepage = "http://search.cpan.org/~drolsky/Devel-StackTrace-2.02/lib/Devel/StackTrace.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Devel-StackTrace-2.02.tar.gz"

    version('2.02', 'bcc49dc2744d1fae906de0de3df07cca')
