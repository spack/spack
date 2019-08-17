# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExceptionClass(PerlPackage):
    """A module that allows you to declare real exception classes in Perl"""

    homepage = "http://search.cpan.org/~drolsky/Exception-Class-1.43/lib/Exception/Class.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Exception-Class-1.43.tar.gz"

    version('1.43', 'ff3fa5c26fa417b68d1f2d0a14cce7f1')

    depends_on('perl-devel-stacktrace', type=('build', 'run'))
    depends_on('perl-class-data-inheritable', type=('build', 'run'))
