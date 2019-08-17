# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlTimeHires(PerlPackage):
    """High resolution alarm, sleep, gettimeofday, interval timers"""

    homepage = "http://search.cpan.org/~jhi/Time-HiRes-1.9746/HiRes.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/J/JH/JHI/Time-HiRes-1.9746.tar.gz"

    version('1.9746', '728dc2c2715313a056792191d7d0726c')
