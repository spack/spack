##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PerlTestMost(PerlPackage):
    """Most commonly needed test functions and features."""

    homepage = "http://search.cpan.org/~ovid/Test-Most-0.35/lib/Test/Most.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OV/OVID/Test-Most-0.35.tar.gz"

    version('0.35', '03dbabd34d6f40af8bd47f5fbb0c6989')

    depends_on('perl-exception-class', type=('build', 'run'))
    depends_on('perl-test-differences', type=('build', 'run'))
    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-test-warn', type=('build', 'run'))
    depends_on('perl-test-deep', type=('build', 'run')) 
