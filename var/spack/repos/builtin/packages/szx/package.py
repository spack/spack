# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Szx(AutotoolsPackage):
    """An ultra fast error bounded compressor for scientific datasets"""

    homepage = "https://github.com/szcompressor/szx"
    url = "https://github.com/szcompressor/szx"
    git = "ssh://git@github.com/szcompressor/szx"

    maintainers = ["robertu94"]

    force_autoreconf = True
    version("main", branch="main")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def configure_args(self):
        args = ["--enable-openmp", "--enable-fortran"]
        return args
