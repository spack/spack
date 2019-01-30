# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTermReadkey(PerlPackage):
    """Term::ReadKey is a compiled perl module dedicated to providing simple
    control over terminal driver modes (cbreak, raw, cooked, etc.,) support
    for non-blocking reads, if the architecture allows, and some generalized
    handy functions for working with terminals. One of the main goals is to
    have the functions as portable as possible, so you can just plug in
    "use Term::ReadKey" on any architecture and have a good likelihood of it
    working."""

    homepage = "http://search.cpan.org/perldoc/Term::ReadKey"
    url = "http://www.cpan.org/authors/id/J/JS/JSTOWE/TermReadKey-2.37.tar.gz"

    version('2.37', 'e8ea15c16333ac4f8d146d702e83cc0c')
