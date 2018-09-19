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


class RFastmatch(RPackage):
    """Package providing a fast match() replacement for cases that require
       repeated look-ups. It is slightly faster that R's built-in match()
       function on first match against a table, but extremely fast on any
       subsequent lookup as it keeps the hash table in memory."""

    homepage = "http://www.rforge.net/fastmatch"
    url      = "https://cran.r-project.org/src/contrib/fastmatch_1.1-0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/fastmatch"

    version('1.1-0', '900c2363c15059ac9d63c4c71ea2d6b2')
