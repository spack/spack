# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMime(RPackage):
    """Guesses the MIME type from a filename extension using the data derived
    from /etc/mime.types in UNIX-type systems."""

    homepage = "https://github.com/yihui/mime"
    url      = "https://cran.r-project.org/src/contrib/mime_0.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mime"

    version('0.5', '87e00b6d57b581465c19ae869a723c4d')
    version('0.4', '789cb33e41db2206c6fc7c3e9fbc2c02')
