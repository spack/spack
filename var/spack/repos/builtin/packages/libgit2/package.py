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


class Libgit2(CMakePackage):
    """libgit2 is a portable, pure C implementation of the Git core
    methods provided as a re-entrant linkable library with a solid
    API, allowing you to write native speed custom Git applications in
    any language which supports C bindings.
    """

    homepage = "https://libgit2.github.com/"
    url      = "https://github.com/libgit2/libgit2/archive/v0.24.2.tar.gz"

    version('0.24.2', '735661b5b73e3c120d13e2bae21e49b3')

    depends_on('cmake@2.8:', type='build')
    depends_on('libssh2')
