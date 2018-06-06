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


class Plplot(CMakePackage):
    """PLplot is a cross-platform package for creating scientific plots."""

    homepage = "http://plplot.sourceforge.net/"
    url      = "https://sourceforge.net/projects/plplot/files/plplot/5.13.0%20Source/plplot-5.13.0.tar.gz/download"

    version('5.13.0', 'bfefeae7fb9a23377c6dc37b44a7da8a')
    version('5.12.0', '998a05be218e5de8f2faf988b8dbdc51')
    version('5.11.0', '632c9e13b09f4e2b2517b3567bc3cece')

    variant('java', default=False, description='Enable Java binding')
    variant('lua', default=False, description='Enable Lua binding')
    variant('pango', default=False, description='Enable Pango')
    variant('python', default=False, description='Enable Python binding')
    variant('qt', default=False, description='Enable QT binding')
    variant('tcl', default=True, description='Enable TCL binding')
    variant('wx', default=False, description='Enable WxWidgets')
    variant('wxold', default=False, description='Use WxWidgets old interface')

    conflicts('~wx', when='+wxold')
    conflicts('+wxold', when='@:5.11')

    depends_on('java', when='+java')
    depends_on('lua', when='+lua')
    depends_on('pango', when='+pango')
    depends_on('py-numpy', type=('build', 'run'), when='+python')
    depends_on('python@2.7:2.8', type=('build', 'run'), when='+python')
    depends_on('qt', when='+qt')
    depends_on('tcl', when='+tcl')
    depends_on('wx', when='+wx')

    depends_on('freetype')
    depends_on('gtkplus')
    depends_on('libx11')
    depends_on('qhull')
    depends_on('swig')

    def cmake_args(self):
        args = []
        # needs 'tk with wish'
        args += ['-DENABLE_tk=OFF']

        if '+java' in self.spec:
            args += ['-DENABLE_java=ON']
        else:
            args += ['-DENABLE_java=OFF']

        if '+lua' in self.spec:
            args += ['-DENABLE_lua=ON']
        else:
            args += ['-DENABLE_lua=OFF']

        if '+python' in self.spec:
            args += ['-DENABLE_python=ON']
        else:
            args += ['-DENABLE_python=OFF']

        if '+qt' in self.spec:
            args += ['-DENABLE_qt=ON']
        else:
            args += ['-DENABLE_qt=OFF']

        if '+tcl' in self.spec:
            args += ['-DENABLE_tcl=ON']
            # could also be addressed by creating the links within tcl
            # as is done for the tclsh executable
            args += [
                '-DTCL_INCLUDE_PATH={0}/include'.format(
                    self.spec['tcl'].prefix.include
                ),
                '-DTCL_LIBRARY={0}'.format(
                    LibraryList(find_libraries(
                        'libtcl*',
                        self.spec['tcl'].prefix.lib,
                        shared=True,
                    )),
                ),
                '-DTCL_STUB_LIBRARY={0}'.format(
                    LibraryList(find_libraries(
                        'libtclstub*',
                        self.spec['tcl'].prefix.lib,
                        shared=False,
                    )),
                )
            ]
        else:
            args += ['-DENABLE_tcl=OFF']

        if '+wx' in self.spec:
            args += ['-DENABLE_wxwidgets=ON']
            if '+wxold' in self.spec:
                args += ['-DOLD_WXWIDGETS=ON']
        else:
            args += ['-DENABLE_wxwidgets=OFF']

        return args
