##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Pgmath(CMakePackage):
    """Flang's math library"""

    homepage = "https://github.com/flang-compiler/flang"
    url      = "https://github.com/flang-compiler/flang/archive/flang_20180612.tar.gz"
    git      = "https://github.com/flang-compiler/flang.git"

    version('develop', branch='master')
    version('20180612', '62284e26214eaaff261a922c67f6878c')

    conflicts("%gcc@:7.1.9999")

    root_cmakelists_dir = 'runtime/libpgmath'
