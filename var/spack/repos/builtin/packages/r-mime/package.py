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


class RMime(RPackage):
    """Guesses the MIME type from a filename extension using the data derived
    from /etc/mime.types in UNIX-type systems."""

    homepage = "https://github.com/yihui/mime"
    url      = "https://cran.r-project.org/src/contrib/mime_0.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mime"

    version('0.5', '87e00b6d57b581465c19ae869a723c4d')
    version('0.4', '789cb33e41db2206c6fc7c3e9fbc2c02')
