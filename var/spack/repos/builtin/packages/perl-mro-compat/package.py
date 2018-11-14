# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlMroCompat(PerlPackage):
    """Provides several utilities for dealing with method resolution order."""

    homepage = "http://search.cpan.org/~haarg/MRO-Compat-0.13/lib/MRO/Compat.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/MRO-Compat-0.13.tar.gz"

    version('0.13', 'd2e603e8ae9dc6934162d190eb085385')
