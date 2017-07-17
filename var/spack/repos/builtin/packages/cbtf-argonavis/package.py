##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


class CbtfArgonavis(CMakePackage):
    """CBTF Argo Navis project contains the CUDA collector and supporting
       libraries that was done as a result of a DOE SBIR grant.

    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"

    # Mirror access template example
    # url = "file:/home/jeg/cbtf-argonavis-1.8.1.tar.gz"
    # version('1.8.1', 'b63db444fff92370a88197882a8d54d0')

    version('1.8', branch='master',
            git='https://github.com/OpenSpeedShop/cbtf-argonavis.git')

    depends_on("cmake@3.0.2:", type='build')
    depends_on("boost@1.50.0:1.59.0")
    depends_on("papi")
    depends_on("mrnet@5.0.1:+lwthreads")
    depends_on("cbtf")
    depends_on("cbtf-krell")
    depends_on("cuda")

    parallel = False

    build_directory = 'build_cbtf_argonavis'

    # We have converted from Package type to CMakePackage type for all the Krell projects.
    # Comments from Pull Request (#4765):
    # CMakePackage is completely different from the old Package class. Previously, you had 
    # a single install() phase to override. Now you have 3 phases: cmake(), build(), and install(). 
    # By default, cmake() runs cmake ... with some common arguments, which you can add to by 
    # overriding cmake_args(). build() runs make, and install() runs make install. 
    # So you need to add the appropriate flags to cmake_args() and remove the calls to make. 
    # See any other CMakePackage for examples.
    # CMakePackage is documented: 
    # http://spack.readthedocs.io/en/latest/spack.build_systems.html?highlight= \
    # CMakePackage#module-spack.build_systems.cmake

    def build_type(self):
        if '+debug' in self.spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        spec = self.spec

        # Look for package installation information in the cbtf and cbtf-krell
        # prefixes
        cmake_prefix_path = join_path(
            spec['cbtf'].prefix) + ':' + join_path(spec['cbtf-krell'].prefix)

        cmake_args = []
        cmake_args.extend(
            ['-DCMAKE_INSTALL_PREFIX=%s' % prefix,
             '-DCMAKE_PREFIX_PATH=%s' % cmake_prefix_path,
             '-DCUDA_DIR=%s' % spec['cuda'].prefix,
             '-DCUDA_INSTALL_PATH=%s' % spec['cuda'].prefix,
             '-DCUDA_TOOLKIT_ROOT_DIR=%s' % spec['cuda'].prefix,
             '-DCUPTI_DIR=%s' % join_path(
                 spec['cuda'].prefix + '/extras/CUPTI'),
             '-DCUPTI_ROOT=%s' % join_path(
                 spec['cuda'].prefix + '/extras/CUPTI'),
             '-DPAPI_ROOT=%s' % spec['papi'].prefix,
             '-DCBTF_DIR=%s' % spec['cbtf'].prefix,
             '-DCBTF_KRELL_DIR=%s' % spec['cbtf-krell'].prefix,
             '-DBOOST_ROOT=%s' % spec['boost'].prefix,
             '-DBoost_DIR=%s' % spec['boost'].prefix,
             '-DBOOST_LIBRARYDIR=%s' % spec['boost'].prefix.lib,
             '-DMRNET_DIR=%s' % spec['mrnet'].prefix,
             '-DBoost_NO_SYSTEM_PATHS=ON'])

        # Add in the standard cmake arguments
        cmake_args.extend(std_cmake_args)

        # Adjust the standard cmake arguments to what we want the build
        # type, etc to be
        self.adjustBuildTypeParams_cmakeOptions(spec, cmake_args)
        return(cmake_args)

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
            if word.startswith('-DCMAKE_VERBOSE_MAKEFILE'):
                cmakeOptions.remove(word)
        BuildTypeOptions.extend([
            '-DCMAKE_VERBOSE_MAKEFILE=ON',
            '-DCMAKE_BUILD_TYPE=None',
            '-DCMAKE_CXX_FLAGS=%s'         % compile_flags,
            '-DCMAKE_C_FLAGS=%s'           % compile_flags
        ])

        cmakeOptions.extend(BuildTypeOptions)

