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
##########################################################################
# Copyright (c) 2015-2016 Krell Institute. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
##########################################################################

from spack import *


class Cbtf(Package):
    """CBTF project contains the base code for CBTF that supports creating
       components, component networks and the support to connect these
       components and component networks into sequential and distributed
       network tools.

    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home"

    # Mirror access template example
    # url      = "file:/home/jeg/cbtf-1.6.tar.gz"
    # version('1.6', 'c1ef4e5aa4e470dffb042abdba0b9987')

    # Use when the git repository is available
    version('1.8', branch='master',
            git='https://github.com/OpenSpeedShop/cbtf.git')

    variant('runtime', default=False,
            description="build only the runtime libraries and collectors.")

    depends_on("cmake@3.0.2:", type='build')
    depends_on("boost@1.50.0:1.59.0")
    depends_on("mrnet@5.0.1:+lwthreads")
    depends_on("xerces-c@3.1.1:")
    # Work around for spack libxml2 package bug, take off python when fixed
    depends_on("libxml2+python")

    parallel = False

    def adjustBuildTypeParams_cmakeOptions(self, spec, cmakeOptions):
        # Sets build type parameters into cmakeOptions the options that will
        # enable the cbtf-krell built type settings

        compile_flags = "-O2 -g"
        BuildTypeOptions = []
        # Set CMAKE_BUILD_TYPE to what cbtf-krell wants it to be, not the
        # stdcmakeargs
        for word in cmakeOptions[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_CXX_FLAGS'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_C_FLAGS'):
                cmakeOptions.remove(word)
        BuildTypeOptions.extend([
            '-DCMAKE_BUILD_TYPE=None',
            '-DCMAKE_CXX_FLAGS=%s'         % compile_flags,
            '-DCMAKE_C_FLAGS=%s'           % compile_flags
        ])

        cmakeOptions.extend(BuildTypeOptions)

    def install(self, spec, prefix):
        with working_dir('build', create=True):

            # Boost_NO_SYSTEM_PATHS  Set to TRUE to suppress searching
            # in system paths (or other locations outside of BOOST_ROOT
            # or BOOST_INCLUDEDIR).  Useful when specifying BOOST_ROOT.
            # Defaults to OFF.

            if '+runtime' in spec:
                # Install message tag include file for use in Intel MIC
                # cbtf-krell build
                # FIXME
                cmakeOptions = []
                cmakeOptions.extend(
                    ['-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                     '-DBoost_NO_SYSTEM_PATHS=TRUE',
                     '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                     '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                     '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                     '-DCMAKE_MODULE_PATH=%s'   % join_path(
                         prefix.share, 'KrellInstitute', 'cmake')])

                # Add in the standard cmake arguments
                cmakeOptions.extend(std_cmake_args)

                # Adjust the standard cmake arguments to what we want the build
                # type, etc to be
                self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

                # Invoke cmake
                cmake('..', *cmakeOptions)

            else:
                cmakeOptions = []
                cmakeOptions.extend(
                    ['-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                     '-DBoost_NO_SYSTEM_PATHS=TRUE',
                     '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                     '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                     '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                     '-DCMAKE_MODULE_PATH=%s'   % join_path(
                         prefix.share, 'KrellInstitute', 'cmake')])

                # Add in the standard cmake arguments
                cmakeOptions.extend(std_cmake_args)

                # Adjust the standard cmake arguments to what we want the build
                # type, etc to be
                self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

                # Invoke cmake
                cmake('..', *cmakeOptions)

            make("clean")
            make()
            make("install")
