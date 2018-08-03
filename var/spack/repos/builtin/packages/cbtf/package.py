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
##########################################################################
# Copyright (c) 2015-2018 Krell Institute. All Rights Reserved.
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


class Cbtf(CMakePackage):
    """CBTF project contains the base code for CBTF that supports creating
       components, component networks and the support to connect these
       components and component networks into sequential and distributed
       network tools.

    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home"
    git      = "https://github.com/OpenSpeedShop/cbtf.git"

    version('develop', branch='master')
    version('1.9.1.1', branch='1.9.1.1')
    version('1.9.1.0', branch='1.9.1.0')

    variant('cti', default=False,
            description="Build MRNet with the CTI startup option")

    variant('runtime', default=False,
            description="build only the runtime libraries and collectors.")

    variant('build_type', default='None', values=('None'),
            description='CMake build type')

    depends_on("cmake@3.0.2:", type='build')

    depends_on("boost@1.66.0", when='@1.9.1.0:9999')
    depends_on("boost@1.50.0:", when='@develop')

    # For MRNet
    depends_on("mrnet@5.0.1-3:+cti", when='@develop+cti')
    depends_on("mrnet@5.0.1-3:+lwthreads", when='@develop')
    depends_on("mrnet@5.0.1-3+cti", when='@1.9.1.0:9999+cti')
    depends_on("mrnet@5.0.1-3+lwthreads", when='@1.9.1.0:9999')

    # For Xerces-C
    depends_on("xerces-c@3.1.1:", when='@develop')
    depends_on("xerces-c@3.1.4:", when='@1.9.1.0:9999')

    # For XML2
    depends_on("libxml2")

    parallel = False

    build_directory = 'build_cbtf'

    def cmake_args(self):

        spec = self.spec

        # Boost_NO_SYSTEM_PATHS  Set to TRUE to suppress searching
        # in system paths (or other locations outside of BOOST_ROOT
        # or BOOST_INCLUDEDIR).  Useful when specifying BOOST_ROOT.
        # Defaults to OFF.

        compile_flags = "-O2 -g"

        if spec.satisfies('+runtime'):

            # Install message tag include file for use in Intel MIC
            # cbtf-krell build
            # FIXME
            cmake_args = [
                '-DCMAKE_CXX_FLAGS=%s'     % compile_flags,
                '-DCMAKE_C_FLAGS=%s'       % compile_flags,
                '-DRUNTIME_ONLY=TRUE',
                '-DBoost_NO_SYSTEM_PATHS=TRUE',
                '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                '-DCMAKE_MODULE_PATH=%s'   % join_path(
                    prefix.share, 'KrellInstitute', 'cmake')]
        else:
            cmake_args = [
                '-DCMAKE_CXX_FLAGS=%s'     % compile_flags,
                '-DCMAKE_C_FLAGS=%s'       % compile_flags,
                '-DBoost_NO_SYSTEM_PATHS=TRUE',
                '-DXERCESC_DIR=%s'         % spec['xerces-c'].prefix,
                '-DBOOST_ROOT=%s'          % spec['boost'].prefix,
                '-DMRNET_DIR=%s'           % spec['mrnet'].prefix,
                '-DCMAKE_MODULE_PATH=%s'   % join_path(
                    prefix.share, 'KrellInstitute', 'cmake')]

        return cmake_args
