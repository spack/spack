##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RRcurl(RPackage):

    """A wrapper for 'libcurl' <http://curl.haxx.se/libcurl/>
    Provides functions to allow one to compose general HTTP requests
    and provides convenient functions to fetch URIs, get & post forms,
    etc. and process the results returned by the Web server. This
    provides a great deal of control over the HTTP/FTP/...
    connection and the form of the request while providing a
    higher-level interface than is available just using R socket
    connections. Additionally, the underlying implementation is
    robust and extensive, supporting FTP/FTPS/TFTP (uploads and
    downloads), SSL/HTTPS, telnet, dict, ldap, and also supports
    cookies, redirects, authentication, etc."""

    homepage = "https://cran.rstudio.com/src/contrib/Archive/RCurl/"
    url      = "https://cran.rstudio.com/src/contrib/Archive/RCurl/RCurl_1.95-0.1.tar.gz"

    version('1.95-4.7', '2d342e5bdcc42a8d4bedcca7740bb504')
    depends_on('r-bitops', type=('build', 'run'))
