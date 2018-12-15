# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlGd(PerlPackage):
    """Interface to Gd Graphics Library"""

    homepage = "http://search.cpan.org/~lds/GD-2.53/GD.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LD/LDS/GD-2.53.tar.gz"

    version('2.53', 'd2c9b18123bcaff8672eb50f2eb37ed3')

    depends_on('perl-module-build', type='build')
    depends_on('perl-extutils-makemaker', type=('build', 'run'))
    depends_on('perl-extutils-pkgconfig', type=('build', 'run'))
    depends_on('libgd')
