# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYoutubeDl(PythonPackage):
    """Command-line program to download videos from YouTube.com and other video
    sites."""

    homepage = "https://github.com/ytdl-org/youtube-dl"
    pypi = "youtube_dl/youtube_dl-2020.3.24.tar.gz"

    license("Unlicense")

    version(
        "2021.12.17",
        sha256="f1336d5de68647e0364a47b3c0712578e59ec76f02048ff5c50ef1c69d79cd55",
        url="https://pypi.org/packages/40/93/65c208f51895f74bbfea1423974c54fff1d1c4e9a97ebee1011b021554b8/youtube_dl-2021.12.17-py2.py3-none-any.whl",
    )
    version(
        "2020.3.24",
        sha256="c0be39ea9bca72fa02a0d2d043c5e9bd8ea8e0fe79705e891161d6fcd29da59e",
        url="https://pypi.org/packages/d0/b3/c3d42f6bbf91da104c272950d30923c222061d7323aa43dcf975a6e8e2c2/youtube_dl-2020.3.24-py2.py3-none-any.whl",
    )
