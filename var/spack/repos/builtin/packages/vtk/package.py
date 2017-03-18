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


class Vtk(CMakePackage):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """

    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/7.1/VTK-7.1.0.tar.gz"

    version('7.1.0', 'a7e814c1db503d896af72458c2d0228f')
    version('7.0.0', '5fe35312db5fb2341139b8e4955c367d')
    version('6.3.0', '0231ca4840408e9dd60af48b314c5b6d')
    version('6.1.0', '25e4dfb3bad778722dcaec80cd5dab7d')

    # VTK7 defaults to OpenGL2 rendering backend
    variant('opengl2', default=True, description='Build with OpenGL2 instead of OpenGL as rendering backend')
    variant('python', default=False, description='Build the python modules')

    patch('gcc.patch', when='@6.1.0')

    depends_on('qt')

    extends('python', when='+python')

    def url_for_version(self, version):
        url = "http://www.vtk.org/files/release/{0}/VTK-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def cmake_args(self):
        spec = self.spec

        opengl_ver = 'OpenGL{0}'.format('2' if '+opengl2' in spec else '')
        qt_ver = spec['qt'].version.up_to(1)
        qt_bin = spec['qt'].prefix.bin

        cmake_args = std_cmake_args[:]
        cmake_args.extend([
            '-DBUILD_SHARED_LIBS=ON',
            '-DVTK_RENDERING_BACKEND:STRING={0}'.format(opengl_ver),

            # Enable/Disable wrappers for Python.
            '-DVTK_WRAP_PYTHON={0}'.format(
                'ON' if '+python' in spec else 'OFF'),

            # Disable wrappers for other languages.
            '-DVTK_WRAP_JAVA=OFF',
            '-DVTK_WRAP_TCL=OFF',

            # Enable Qt support here.
            '-DVTK_QT_VERSION:STRING={0}'.format(qt_ver),
            '-DQT_QMAKE_EXECUTABLE:PATH={0}/qmake'.format(qt_bin),
            '-DVTK_Group_Qt:BOOL=ON',
        ])

        # NOTE: The following definitions are required in order to allow
        # VTK to build with qt~webkit versions (see the documentation for
        # more info: http://www.vtk.org/Wiki/VTK/Tutorials/QtSetup).
        if '~webkit' in spec['qt']:
            cmake_args.extend([
                '-DVTK_Group_Qt:BOOL=OFF',
                '-DModule_vtkGUISupportQt:BOOL=ON',
                '-DModule_vtkGUISupportQtOpenGL:BOOL=ON',
            ])

        if spec.satisfies('@:6.1.0'):
            cmake_args.append('-DCMAKE_C_FLAGS=-DGLX_GLXEXT_LEGACY')
            cmake_args.append('-DCMAKE_CXX_FLAGS=-DGLX_GLXEXT_LEGACY')

        return cmake_args
