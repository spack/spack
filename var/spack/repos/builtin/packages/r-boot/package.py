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


class RBoot(RPackage):
    """Functions and datasets for bootstrapping from the book "Bootstrap
    Methods and Their Application" by A. C. Davison and D. V. Hinkley (1997,
    CUP), originally written by Angelo Canty for S."""

    homepage = "https://cran.r-project.org/package=boot"
    url      = "https://cran.r-project.org/src/contrib/boot_1.3-18.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/boot"

    version('1.3-20', 'bb879fb4204a4f94ab82c98dd1ad5eca')
    version('1.3-18', '711dd58af14e1027eb8377d9202e9b6f')
