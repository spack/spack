# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTextSimpletable(PerlPackage):
    """Simple Eyecandy ASCII Tables"""

    homepage = "http://search.cpan.org/~mramberg/Text-SimpleTable/lib/Text/SimpleTable.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MR/MRAMBERG/Text-SimpleTable-2.04.tar.gz"

    version('2.04', '550136523c8da37b616988f9a5f58d59')
