# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYtDlp(PythonPackage):
    """yt-dlp is a command-line program to download videos from websites, chiefly youtube.com;
    it is a youtube-dl fork focused on adding new features and patches"""

    homepage = "https://github.com/yt-dlp/yt-dlp"
    pypi = "yt-dlp/yt-dlp-2023.7.6.tar.gz"

    version("2023.7.6", sha256="cb58373869c8ccb5034746f91cfccd6d25ea697090dfd6f93e9034d51eb4aed2")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("ffmpeg+openssl", type="run")
