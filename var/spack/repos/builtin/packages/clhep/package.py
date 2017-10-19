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


class Clhep(CMakePackage):
    """CLHEP is a C++ Class Library for High Energy Physics. """
    homepage = "http://proj-clhep.web.cern.ch/proj-clhep/"
    url      = "http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/clhep-2.2.0.5.tgz"
    list_url = "https://proj-clhep.web.cern.ch/proj-clhep/"
    list_depth = 1

    version('2.3.4.4', '8b8a33d0d19213b60d6c22ce5fc93761')
    version('2.3.4.3', '6941279f70d69492fff1aa955f3f2562')
    version('2.3.4.2', '1e7a9046c9ad0b347d6812f8031191da')
    version('2.3.4.1', '5ae85571ff3d8b2c481c3f95ea89b751')
    version('2.3.4.0', 'dd899d0791a823221927f97edf190348')
    version('2.3.3.2', '8b9f8d7f4dccec6d058b3a078f66b6a3')
    version('2.3.3.1', '456ef9d262ef4e776af984bfbe2f48c7')
    version('2.3.3.0', '3637eaa6750606e589e52c9e155a382e')
    version('2.3.2.2', '567b304b0fa017e1e9fbf199f456ebe9')
    version('2.3.2.1', '064903cb5c23b54f520d04ca6230b901')
    version('2.3.1.1', '16efca7641bc118c9d217cc96fe90bf5')
    version('2.3.1.0', 'b084934fc26a4182a08c09c292e19161')
    version('2.3.0.0', 'a00399a2ca867f2be902c22fc71d7e2e')
    version('2.2.0.8', '5a23ed3af785ac100a25f6cb791846af')
    version('2.2.0.5', '1584e8ce6ebf395821aed377df315c7c')
    version('2.2.0.4', '71d2c7c2e39d86a0262e555148de01c1')

    variant('cxx11', default=True, description="Compile using c++11 dialect.")
    variant('cxx14', default=False, description="Compile using c++14 dialect.")

    depends_on('cmake@2.8.12.2:', when='@2.2.0.4:2.3.0.0', type='build')
    depends_on('cmake@3.2:', when='@2.3.0.1:', type='build')

    def patch(self):
        filter_file('SET CMP0042 OLD',
                    'SET CMP0042 NEW',
                    '%s/%s/CLHEP/CMakeLists.txt'
                    % (self.stage.path, self.spec.version))

    root_cmakelists_dir = 'CLHEP'

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if '+cxx11' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx11_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx11_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx11_flag)

        if '+cxx14' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx14_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx14_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx14_flag)

        return cmake_args
