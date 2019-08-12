# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextUnidecode(PerlPackage):
    """plain ASCII transliterations of Unicode text"""

    homepage = "http://search.cpan.org/~sburke/Text-Unidecode/lib/Text/Unidecode.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SB/SBURKE/Text-Unidecode-1.30.tar.gz"

    version('1.30', '31cca8505bd74ed9d8036cdc84c808ca')
