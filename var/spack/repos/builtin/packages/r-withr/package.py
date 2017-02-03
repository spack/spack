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


class RWithr(RPackage):
    """A set of functions to run code 'with' safely and temporarily modified
    global state. Many of these functions were originally a part of the
    'devtools' package, this provides a simple package with limited
    dependencies to provide access to these functions."""

    homepage = "http://github.com/jimhester/withr"
    url      = "https://cran.r-project.org/src/contrib/withr_1.0.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/withr"

    version('1.0.2', 'ca52b729af9bbaa14fc8b7bafe38663c')
    version('1.0.1', 'ac38af2c6f74027c9592dd8f0acb7598')

    depends_on('r@3.0.2:')
