# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDownloader(RPackage):
    """Provides a wrapper for the download.file function, making it possible to
       download files over HTTPS on Windows, Mac OS X, and other Unix-like
       platforms. The 'RCurl' package provides this functionality
       (and much more) but can be difficult to install because it must be
       compiled with external dependencies. This package has no external
       dependencies, so it is much easier to install."""

    homepage = "https://cran.rstudio.com/web/packages/downloader/index.html"
    url      = "https://cran.rstudio.com/src/contrib/downloader_0.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/downloader"

    version('0.4', 'f26daf8fbeb29a1882bf102f62008594')

    depends_on('r-digest', type=('build', 'run'))
