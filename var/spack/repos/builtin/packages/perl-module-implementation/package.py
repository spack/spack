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


class PerlModuleImplementation(PerlPackage):
    """Loads one of several alternate underlying implementations for a
    module"""

    homepage = "http://search.cpan.org/~drolsky/Module-Implementation/lib/Module/Implementation.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Module-Implementation-0.09.tar.gz"

    version('0.09', '52e3fe0ca6b1eff0488d59b7aacc0667')

    depends_on('perl-module-runtime', type=('build', 'run'))
    depends_on('perl-test-fatal', type=('build', 'run'))
    depends_on('perl-test-requires', type=('build', 'run'))
    depends_on('perl-try-tiny', type=('build', 'run'))
