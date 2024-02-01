# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Usearch(Package):
    """USEARCH is a unique sequence analysis tool with thousands of users
    world-wide.

    Note: A manual download is required for USEARCH.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.drive5.com/usearch/"
    maintainers("snehring")

    manual_download = True

    version("11.0.667", sha256="1be0faa1380100296029064e4cf9665d723d43f03c794da444c5b1a6b6799ac2")
    version("10.0.240", sha256="297ba03cb5bdc60c9727b7949cc08bfeecad8b290c2844b5ad011f72a7e1399c")

    def url_for_version(self, version):
        return "file://{0}/usearch{1}_i86linux32.gz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("usearch{0}_i86linux32".format(self.version), prefix.bin.usearch)
        set_executable(prefix.bin.usearch)
