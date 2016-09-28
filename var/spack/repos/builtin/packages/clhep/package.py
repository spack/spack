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


class Clhep(Package):
    """CLHEP is a C++ Class Library for High Energy Physics. """
    homepage = "http://proj-clhep.web.cern.ch/proj-clhep/"
    url      = "http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/clhep-2.2.0.5.tgz"
    list_url = "https://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/"

    version('2.3.2.2', '567b304b0fa017e1e9fbf199f456ebe9')
    version('2.3.1.1', '16efca7641bc118c9d217cc96fe90bf5')
    version('2.3.1.0', 'b084934fc26a4182a08c09c292e19161')
    version('2.3.0.0', 'a00399a2ca867f2be902c22fc71d7e2e')
    version('2.2.0.8', '5a23ed3af785ac100a25f6cb791846af')
    version('2.2.0.5', '1584e8ce6ebf395821aed377df315c7c')
    version('2.2.0.4', '71d2c7c2e39d86a0262e555148de01c1')

    variant('debug', default=False, description="Switch to the debug version of CLHEP.")
    variant('cxx11', default=True, description="Compile using c++11 dialect.")
    variant('cxx14', default=False, description="Compile using c++14 dialect.")

    depends_on('cmake@2.8.12.2:', when='@2.2.0.4:2.3.0.0', type='build')
    depends_on('cmake@3.2:', when='@2.3.0.1:', type='build')

    def patch(self):
        filter_file('SET CMP0042 OLD',
                    'SET CMP0042 NEW',
                    '%s/%s/CLHEP/CMakeLists.txt'
                    % (self.stage.path, self.spec.version))

    def install(self, spec, prefix):
        # Handle debug
        # Pull out the BUILD_TYPE so we can change it (Release is default)
        cmake_args = [arg for arg in std_cmake_args if 'BUILD_TYPE' not in arg]
        build_type = 'Debug' if '+debug' in spec else 'MinSizeRel'
        cmake_args.extend(['-DCMAKE_BUILD_TYPE=' + build_type])

        if '+cxx11' in spec:
            env['CXXFLAGS'] = self.compiler.cxx11_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx11_flag)

        if '+cxx14' in spec:
            env['CXXFLAGS'] = self.compiler.cxx14_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx14_flag)

        # Note that the tar file is unusual in that there's a
        # CLHEP directory (addtional layer)
        cmake_args.append("../CLHEP")

        # Run cmake in a build directory
        with working_dir('build', create=True):
            cmake(*cmake_args)
            make()
            make("install")
