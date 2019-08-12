# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlNetScpExpect(PerlPackage):
    """Wrapper for scp that allows passwords via Expect."""

    homepage = "http://search.cpan.org/~rybskej/Net-SCP-Expect/Expect.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RY/RYBSKEJ/Net-SCP-Expect-0.16.tar.gz"

    version('0.16', 'a3d8f5e6a34ba3df8527aea098f64a58')
