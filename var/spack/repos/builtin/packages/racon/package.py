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


class Racon(CMakePackage):
    """Ultrafast consensus module for raw de novo genome assembly of long
     uncorrected reads."""

    homepage = "https://github.com/isovic/racon"
    url      = "https://github.com/isovic/racon/releases/download/1.2.1/racon-v1.2.1.tar.gz"

    version('1.3.0', 'e00d61f391bce2af20ebd2a3aee1e05a')
    version('1.2.1', '7bf273b965a5bd0f41342a9ffe5c7639')

    depends_on('cmake@3.2:', type='build')
    depends_on('python', type='build')

    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.1')

    def cmake_args(self):
        args = ['-Dracon_build_wrapper=ON']
        return args

    def install(self, spec, prefix):
        install_tree('spack-build/bin', prefix.bin)
        install_tree('spack-build/lib', prefix.lib)
