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


class RRprojroot(RPackage):
    """Robust, reliable and flexible paths to files below a project root.
    The 'root' of a project is defined as a directory that matches a certain
    criterion, e.g., it contains a certain regular file."""

    homepage = "https://github.com/krlmlr/rprojroot"
    url      = "https://cran.r-project.org/src/contrib/rprojroot_1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rprojroot"

    version('1.2', 'c1a0574aaac2a43a72f804abbaea19c3')

    depends_on('r@3.0.0:')

    depends_on('r-backports', type=('build', 'run'))
