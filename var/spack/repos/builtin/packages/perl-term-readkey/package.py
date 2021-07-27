# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTermReadkey(PerlPackage):
    """Term::ReadKey is a compiled perl module dedicated to providing simple
    control over terminal driver modes (cbreak, raw, cooked, etc.,) support
    for non-blocking reads, if the architecture allows, and some generalized
    handy functions for working with terminals."""
    homepage = "https://metacpan.org/pod/Term::ReadKey"
    url      = "https://cpan.metacpan.org/authors/id/J/JS/JSTOWE/TermReadKey-2.38.tar.gz"

    version('2.38', sha256='5a645878dc570ac33661581fbb090ff24ebce17d43ea53fd22e105a856a47290')
