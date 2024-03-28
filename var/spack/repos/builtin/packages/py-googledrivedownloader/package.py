# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGoogledrivedownloader(PythonPackage):
    """Minimal class to download shared files from Google Drive."""

    homepage = "https://github.com/ndrplz/google-drive-downloader"
    pypi = "googledrivedownloader/googledrivedownloader-0.4.tar.gz"

    license("MIT")

    version(
        "0.4",
        sha256="26ef906c4a038de6fb36f375b0cb0af6f0b6d7ea9ce019a3a08abc50fd6a3b73",
        url="https://pypi.org/packages/3a/5c/485e8724383b482cc6c739f3359991b8a93fb9316637af0ac954729545c9/googledrivedownloader-0.4-py2.py3-none-any.whl",
    )
