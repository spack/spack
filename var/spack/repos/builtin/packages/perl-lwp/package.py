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


class PerlLwp(PerlPackage):
    """The World-Wide Web library for Perl"""

    homepage = "http://search.cpan.org/~oalders/libwww-perl-6.29/lib/LWP.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/libwww-perl-6.29.tar.gz"

    version('6.29', 'efec8d563ffd3652333356aa722c2b56')

    depends_on('perl-test-requiresinternet', type=('build', 'run'))
    depends_on('perl-http-message', type=('build', 'run'))
    depends_on('perl-file-listing', type=('build', 'run'))
    depends_on('perl-http-daemon', type=('build', 'run'))
    depends_on('perl-html-parser', type=('build', 'run'))
    depends_on('perl-http-cookies', type=('build', 'run'))
    depends_on('perl-www-robotrules', type=('build', 'run'))
    depends_on('perl-test-fatal', type=('build', 'run'))
    depends_on('perl-http-negotiate', type=('build', 'run'))
    depends_on('perl-net-http', type=('build', 'run'))
