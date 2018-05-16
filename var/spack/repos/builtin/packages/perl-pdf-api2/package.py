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


class PerlPdfApi2(PerlPackage):
    """Facilitates the creation and modification of PDF files"""

    homepage = "http://search.cpan.org/~ssimms/PDF-API2-2.033/lib/PDF/API2.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SS/SSIMMS/PDF-API2-2.033.tar.gz"

    version('2.033', '4223a38add42741f996bd67d5f2f8e5b')

    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-test-memory-cycle', type=('build', 'run'))
    depends_on('perl-font-ttf', type=('build', 'run'))
