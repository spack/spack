# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoogleDriveDownloader(PythonPackage):
    """Minimal class to download shared files from Google
    Drive."""

    homepage = "https://github.com/ndrplz/google-drive-downloader"
    url      = "https://github.com/ndrplz/google-drive-downloader/archive/0.2.tar.gz"

    version('0.2', sha256='093d37242b632aa6204a4ffb7f41d44108c2b0687895b717003440385493d3e6')
