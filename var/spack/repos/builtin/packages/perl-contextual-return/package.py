# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlContextualReturn(PerlPackage):
    """Create context-sensitive return values"""

    homepage = "http://search.cpan.org/~dconway/Contextual-Return/lib/Contextual/Return.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DC/DCONWAY/Contextual-Return-0.004014.tar.gz"

    version('0.004014', '5cb31f1637c17af6a8e5b852d820af79')

    depends_on('perl-want')
