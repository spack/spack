# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    version('3.0', '741202626eacd1f9c022b0a4d7be6d6a')
    version('2.3',   '7250ee8caed98ba76906ab4d32da60f8')
    version('1.0',   '93d34926d6071e1fba7e728b482f0dd9')
    version('0.9.7', 'a101f7de948cb828fef571c730f39217')

    depends_on('r@3.0.0:')
    depends_on('curl')
