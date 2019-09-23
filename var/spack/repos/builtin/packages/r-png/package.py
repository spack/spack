# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPng(RPackage):
    """This package provides an easy and simple way to read, write and display
    bitmap images stored in the PNG format. It can read and write both files
    and in-memory raw vectors."""

    homepage = "http://www.rforge.net/png/"
    url      = "https://cloud.r-project.org/src/contrib/png_0.1-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/png"

    version('0.1-7', '1ebc8b8aa5979b12c5ec2384b30d649f')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('libpng')
