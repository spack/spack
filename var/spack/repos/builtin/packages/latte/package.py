##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Latte(CMakePackage):
    """Open source density functional tight binding molecular dynamics."""

    homepage = "https://gitlab.com/exaalt/latte"
    url      = "https://gitlab.com/exaalt/latte/tags/v1.0"

    version('develop', git='https://gitlab.com/exaalt/latte', branch='cmake')

    depends_on("cmake@3.1:", type='build')
    depends_on('blas')
    depends_on('lapack')

    root_cmakelists_dir = 'cmake'

    def cmake_args(self):
        options = ['-DBUILD_SHARED_LIBS=ON']

        return options
