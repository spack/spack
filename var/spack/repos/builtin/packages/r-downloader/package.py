# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://cloud.r-project.org/package=downloader"
    url      = "https://cloud.r-project.org/src/contrib/downloader_0.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/downloader"

    version('0.4', 'f26daf8fbeb29a1882bf102f62008594')

    depends_on('r-digest', type=('build', 'run'))
