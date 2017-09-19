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


class RZlibbioc(RPackage):
    """This package uses the source code of zlib-1.2.5 to create libraries
       for systems that do not have these available via other means (most
       Linux and Mac users should have system-level access to zlib, and no
       direct need for this package). See the vignette for instructions
       on use."""

    homepage = ("http://bioconductor.org/packages/release"
                "/bioc/html/Zlibbioc.html")
    url      = ("https://bioconductor.org/packages/3.5/bioc"
                "/src/contrib/zlibbioc_1.22.0.tar.gz")

    version('1.22.0', '2e9496b860270d2e73d1305b8c6c69a5')
