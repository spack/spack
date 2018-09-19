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


class PerlHttpMessage(PerlPackage):
    """HTTP style message (base class)"""

    homepage = "http://search.cpan.org/~oalders/HTTP-Message-6.13/lib/HTTP/Status.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Message-6.13.tar.gz"

    version('6.13', '4c1b7c6ee114c1cff69379ec9651d9ac')

    depends_on('perl-lwp-mediatypes', type=('build', 'run'))
    depends_on('perl-encode-locale', type=('build', 'run'))
    depends_on('perl-io-html', type=('build', 'run'))
    depends_on('perl-try-tiny', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-http-date', type=('build', 'run'))
