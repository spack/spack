# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDbfile(PerlPackage):
    """DB_File is a module which allows Perl programs to make use of the
    facilities provided by Berkeley DB version 1.x (if you have a newer version
    of DB, see "Using DB_File with Berkeley DB version 2 or greater").
    It is assumed that you have a copy of the Berkeley DB manual pages at hand
    when reading this documentation. The interface defined here mirrors the
    Berkeley DB interface closely."""

    homepage = "https://metacpan.org/pod/DB_File"
    url      = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/DB_File-1.840.tar.gz"

    version('1.840', '8a2e98d457a216840ac893913c24141e')

    depends_on('perl-extutils-makemaker', type='build')
