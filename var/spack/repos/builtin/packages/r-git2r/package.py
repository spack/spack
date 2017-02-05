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


class RGit2r(RPackage):
    """Interface to the 'libgit2' library, which is a pure C implementation of
    the 'Git' core methods. Provides access to 'Git' repositories to extract
    data and running some basic 'Git' commands."""

    homepage = "https://github.com/ropensci/git2r"
    url      = "https://cran.r-project.org/src/contrib/git2r_0.18.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/git2r"

    version('0.18.0', 'fb5741eb490c3d6e23a751a72336f24d')
    version('0.15.0', '57658b3298f9b9aadc0dd77b4ef6a1e1')

    depends_on('r@3.0.2:')

    depends_on('zlib')
    depends_on('openssl')
