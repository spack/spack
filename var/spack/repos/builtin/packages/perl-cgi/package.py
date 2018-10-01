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


class PerlCgi(PerlPackage):
    """CGI - Handle Common Gateway Interface requests and responses

       CGI was included in the Perl distribution from 5.4 to 5.20 but
       has since been removed."""

    homepage = "https://metacpan.org/pod/CGI"
    url      = "https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-4.40.tar.gz"

    version('4.40', sha256='10efff3061b3c31a33b3cc59f955aef9c88d57d12dbac46389758cef92f24f56')
    version('4.39', sha256='7e73417072445f24e03d63802ed3a9e368c9b103ddc96e2a9bcb6a251215fb76')
    version('4.38', sha256='8c58f4a529bb92a914b22b7e64c5e31185c9854a4070a6dfad44fe5cc248e7d4')
    version('4.37', sha256='7a14eee5df640f7141848f653cf48d99bfc9b5c68e18167338ee01b91cdfb883')

    depends_on('perl-html-parser', type=('build', 'run'))
