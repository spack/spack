# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlDataDumper(PerlPackage):
    """Stringified perl data structures, suitable for both printing and eval"""

    homepage = "http://search.cpan.org/dist/Data-Dumper/Dumper.pm"
    url      = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/Data-Dumper-2.173.tar.gz"

    version('2.173', '5e57ded19aff069f3f05dfb5e5ca1e1d')
