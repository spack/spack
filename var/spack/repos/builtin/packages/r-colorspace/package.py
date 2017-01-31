##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RColorspace(RPackage):
    """Carries out mapping between assorted color spaces including RGB, HSV,
    HLS, CIEXYZ, CIELUV, HCL (polar CIELUV), CIELAB and polar CIELAB.
    Qualitative, sequential, and diverging color palettes based on HCL colors
    are provided."""

    homepage = "https://cran.r-project.org/web/packages/colorspace/index.html"
    url      = "https://cran.r-project.org/src/contrib/colorspace_1.3-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/colorspace"

    version('1.3-2', '63000bab81d995ff167df76fb97b2984')
    version('1.2-6', 'a30191e9caf66f77ff4e99c062e9dce1')
