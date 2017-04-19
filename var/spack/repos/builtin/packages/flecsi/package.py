##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Flecsi(CMakePackage):
    """FleCSI is a compile-time configurable framework designed to support
       multi-physics application development. As such, FleCSI attempts to
       provide a very general set of infrastructure design patterns that can
       be specialized and extended to suit the needs of a broad variety of
       solver and data requirements. Current support includes multi-dimensional
       mesh topology, mesh geometry, and mesh adjacency information,
       n-dimensional hashed-tree data structures, graph partitioning
       interfaces,and dependency closures.
    """
    homepage = "http://flecsi.lanl.gov/"
    url      = "https://github.com/laristra/flecsi/tarball/v1.0"

    version('develop', git='https://github.com/laristra/flecsi', branch='master', submodules=True)

    variant('debug', default=False, description='Build debug version')

    depends_on("cmake@3.1:", type='build')
    depends_on("legion")

    # drop when #3779 has been fixed
    def do_fetch(self, mirror_only=True):
        super(Flecsi, self).do_fetch(mirror_only)
        git = which("git")
        git('-C', 'flecsi', 'submodule', 'update', '--init', '--recursive',
            '--depth=1')

    def build_type(self):
        spec = self.spec
        if '+debug' in spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        return ['-DENABLE_UNIT_TESTS=ON']
