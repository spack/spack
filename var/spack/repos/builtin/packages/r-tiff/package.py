# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTiff(RPackage):
    """This package provides an easy and simple way to read, write and
       display bitmap images stored in the TIFF format. It can read and
       write both files and in-memory raw vectors."""

    homepage = "http://www.rforge.net/tiff/"
    url      = "https://cran.rstudio.com/src/contrib/tiff_0.1-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tiff"

    version('0.1-5', '5052990b8647c77d3e27bc0ecf064e0b')

    depends_on("libjpeg")
    depends_on("libtiff")
