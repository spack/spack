##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RCurl(RPackage):
    """The curl() and curl_download() functions provide highly configurable
    drop-in replacements for base url() and download.file() with better
    performance, support for encryption (https, ftps), gzip compression,
    authentication, and other libcurl goodies. The core of the package
    implements a framework for performing fully customized requests where data
    can be processed either in memory, on disk, or streaming via the callback
    or connection interfaces. Some knowledge of libcurl is recommended; for a
    more-user-friendly web client see the 'httr' package which builds on this
    package with http specific tools and logic."""

    homepage = "https://github.com/jeroenooms/curl"
    url      = "https://cran.r-project.org/src/contrib/curl_2.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/curl"

    version('2.3',   '7250ee8caed98ba76906ab4d32da60f8')
    version('1.0',   '93d34926d6071e1fba7e728b482f0dd9')
    version('0.9.7', 'a101f7de948cb828fef571c730f39217')

    depends_on('r@3.0.0:')
    depends_on('curl')
