# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlClassLoad(PerlPackage):
    """A working (require "Class::Name") and more"""

    homepage = "http://search.cpan.org/~ether/Class-Load-0.24/lib/Class/Load.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-0.24.tar.gz"

    version('0.24', 'daf8aeedf4d19ed6d3f75cd3e720116d')
