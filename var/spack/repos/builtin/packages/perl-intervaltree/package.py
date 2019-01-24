# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlIntervaltree(PerlPackage):
    """Set::IntervalTree uses Interval Trees to store and efficiently look up
    ranges using a range-based lookup."""

    homepage = "https://metacpan.org/release/Set-IntervalTree"
    url      = "https://cpan.metacpan.org/authors/id/B/BE/BENBOOTH/Set-IntervalTree-0.10.tar.gz"

    version('0.10', '42efe9369f1b30e7fd04e10c07226b06')

    depends_on('perl-extutils-makemaker', type='build')
