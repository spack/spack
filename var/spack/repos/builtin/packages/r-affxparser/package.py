##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RAffxparser(RPackage):
    """Package for parsing Affymetrix files (CDF, CEL, CHP, BPMAP, BAR).
    It provides methods for fast and memory efficient parsing of
    Affymetrix files using the Affymetrix' Fusion SDK. Both ASCII-
    and binary-based files are supported. Currently, there are methods
    for reading chip definition file (CDF) and a cell intensity file (CEL).
    These files can be read either in full or in part. For example,
    probe signals from a few probesets can be extracted very quickly
    from a set of CEL files into a convenient list structure."""

    homepage = "https://www.bioconductor.org/packages/affxparser/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/affxparser_1.48.0.tar.gz"
    list_url = homepage

    version('1.48.0', '20ae3f61e3ea25c3baeabf949b1f1165')
