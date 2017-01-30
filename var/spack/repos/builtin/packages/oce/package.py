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
import platform


class Oce(Package):
    """Open CASCADE Community Edition:
    patches/improvements/experiments contributed by users over the official
    Open CASCADE library.
    """
    homepage = "https://github.com/tpaviot/oce"

    version('0.18',   '226e45e77c16a4a6e127c71fefcd171410703960ae75c7ecc7eb68895446a993')
    version('0.17.2', 'bf2226be4cd192606af677cf178088e5')
    version('0.17.1', '36c67b87093c675698b483454258af91')
    version('0.17',   'f1a89395c4b0d199bea3db62b85f818d')
    version('0.16.1', '4d591b240c9293e879f50d86a0cb2bb3')
    version('0.16',   '7a4b4df5a104d75a537e25e7dd387eca')

    variant('tbb', default=True,
            description='Build with Intel Threading Building Blocks')

    depends_on('cmake@2.8:', type='build')
    depends_on('tbb', when='+tbb')

    def url_for_version(self, version):
        return 'https://github.com/tpaviot/oce/archive/OCE-%s.tar.gz' % (
            version.dotted)

    # There is a bug in OCE which appears with Clang (version?) or GCC 6.0
    # and has to do with compiler optimization, see
    # https://github.com/tpaviot/oce/issues/576
    # http://tracker.dev.opencascade.org/view.php?id=26042
    # https://github.com/tpaviot/oce/issues/605
    # https://github.com/tpaviot/oce/commit/61cb965b9ffeca419005bc15e635e67589c421dd.patch
    patch('null.patch', when='@0.16:0.17.1')

    # fix build with Xcode 8 "previous definition of CLOCK_REALTIME"
    # reported 27 Sep 2016 https://github.com/tpaviot/oce/issues/643
    if (platform.system() == "Darwin") and (
       '.'.join(platform.mac_ver()[0].split('.')[:2]) == '10.12'):
        patch('sierra.patch', when='@0.17.2:0.18')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.extend([
            '-DOCE_INSTALL_PREFIX=%s' % prefix,
            '-DOCE_BUILD_SHARED_LIB:BOOL=ON',
            '-DCMAKE_BUILD_TYPE:STRING=Release',
            '-DOCE_DATAEXCHANGE:BOOL=ON',
            '-DOCE_DISABLE_X11:BOOL=ON',
            '-DOCE_DRAW:BOOL=OFF',
            '-DOCE_MODEL:BOOL=ON',
            '-DOCE_MULTITHREAD_LIBRARY:STRING=%s' % (
                'TBB' if '+tbb' in spec else 'NONE'),
            '-DOCE_OCAF:BOOL=ON',
            '-DOCE_USE_TCL_TEST_FRAMEWORK:BOOL=OFF',
            '-DOCE_VISUALISATION:BOOL=OFF',
            '-DOCE_WITH_FREEIMAGE:BOOL=OFF',
            '-DOCE_WITH_GL2PS:BOOL=OFF',
            '-DOCE_WITH_OPENCL:BOOL=OFF'
        ])

        if platform.system() == 'Darwin':
            options.extend([
                '-DOCE_OSX_USE_COCOA:BOOL=ON',
            ])

        if '.'.join(platform.mac_ver()[0].split('.')[:2]) == '10.12':
            # use @rpath on Sierra due to limit of dynamic loader
            options.append('-DCMAKE_MACOSX_RPATH=ON')
        else:
            options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        cmake('.', *options)
        make("install/strip")
        if self.run_tests:
            make("test")
