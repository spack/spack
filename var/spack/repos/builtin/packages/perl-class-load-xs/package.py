# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlClassLoadXs(PerlPackage):
    """This module provides an XS implementation for portions of
       Class::Load."""

    homepage = "http://search.cpan.org/~ether/Class-Load-XS-0.10/lib/Class/Load/XS.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-XS-0.10.tar.gz"

    version('0.10', '2c15488b5b28afadbb5315e44a721e05')

    depends_on('perl-class-load', type=('build', 'run'))
