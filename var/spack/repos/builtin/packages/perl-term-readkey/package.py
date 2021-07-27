# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTermReadkey(PerlPackage):
    homepage = "https://metacpan.org/pod/Term::ReadKey"
    url      = "https://cpan.metacpan.org/authors/id/J/JS/JSTOWE/TermReadKey-2.38.tar.gz"

    version('2.38', sha256='5a645878dc570ac33661581fbb090ff24ebce17d43ea53fd22e105a856a47290')
