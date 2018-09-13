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


class RMmwrweek(RPackage):
    """The first day of any MMWR week is Sunday. MMWR week numbering is
    sequential beginning with 1 and incrementing with each week to a maximum
    of 52 or 53. MMWR week #1 of an MMWR year is the first week of the year
    that has at least four days in the calendar year. This package provides
    functionality to convert Dates to MMWR day, week, and year and the
    reverse."""

    homepage = "https://cran.r-project.org/package=MMWRweek"
    url      = "https://cran.r-project.org/src/contrib/MMWRweek_0.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/MMWRweek"

    version('0.1.1', 'a1245025126f8a96c72be8f7b06b0499')
