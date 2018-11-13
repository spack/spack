# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExtutilsDepends(PerlPackage):
    """Easily build XS extensions that depend on XS extensions"""

    homepage = "http://search.cpan.org/~xaoc/ExtUtils-Depends/lib/ExtUtils/Depends.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-Depends-0.405.tar.gz"

    version('0.405', 'caefbca2f173d0cea3f5ac26b6c08a2c')
