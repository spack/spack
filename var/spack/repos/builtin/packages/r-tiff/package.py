# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTiff(RPackage):
    """This package provides an easy and simple way to read, write and
       display bitmap images stored in the TIFF format. It can read and
       write both files and in-memory raw vectors."""

    homepage = "http://www.rforge.net/tiff/"
    url      = "https://cloud.r-project.org/src/contrib/tiff_0.1-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tiff"

    version('0.1-5', '5052990b8647c77d3e27bc0ecf064e0b')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on("jpeg")
    depends_on("libtiff")
