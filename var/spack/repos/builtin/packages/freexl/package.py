# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Freexl(AutotoolsPackage):
    """FreeXL is an open source library to extract valid data from within
       an Excel (.xls) spreadsheet."""

    homepage = "http://www.gaia-gis.it"
    url      = "http://www.gaia-gis.it/gaia-sins/freexl-1.0.5.tar.gz"

    version('1.0.5', '3ed2a0486f03318820b25f0ccae5e14d')
