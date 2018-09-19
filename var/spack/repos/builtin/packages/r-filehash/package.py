##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class RFilehash(RPackage):
    """Implements a simple key-value style database where character string keys
    are associated with data values that are stored on the disk. A simple
    interface is provided for inserting, retrieving, and deleting data from the
    database. Utilities are provided that allow 'filehash' databases to be
    treated much like environments and lists are already used in R. These
    utilities are provided to encourage interactive and exploratory analysis on
    large datasets. Three different file formats for representing the database
    are currently available and new formats can easily be incorporated by third
    parties for use in the 'filehash' framework."""

    homepage = 'https://cran.r-project.org/'
    url      = "https://cran.r-project.org/src/contrib/filehash_2.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/filehash"

    version('2.3', '01fffafe09b148ccadc9814c103bdc2f')
