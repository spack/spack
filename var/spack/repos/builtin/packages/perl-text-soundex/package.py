# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextSoundex(PerlPackage):
    """Soundex is a phonetic algorithm for indexing names by sound, as
       pronounced in English. The goal is for names with the same
       pronunciation to be encoded to the same representation so
       that they can be matched despite minor differences in spelling"""

    homepage = "http://search.cpan.org/~rjbs/Text-Soundex-3.05/Soundex.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Text-Soundex-3.05.tar.gz"

    version('3.05', 'cb40ded7a5d27aa3a411d274d6ec18ae')
