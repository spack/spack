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


class Vtk(Package):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """
    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/6.1/VTK-6.1.0.tar.gz"

    version("7.0.0", "5fe35312db5fb2341139b8e4955c367d",
            url="http://www.vtk.org/files/release/7.0/VTK-7.0.0.tar.gz")

    version("6.3.0", '0231ca4840408e9dd60af48b314c5b6d',
            url="http://www.vtk.org/files/release/6.3/VTK-6.3.0.tar.gz")

    version('6.1.0', '25e4dfb3bad778722dcaec80cd5dab7d')

    patch("gcc.patch")

    extends('python', when='+python')
    depends_on('python', when='+python')
    depends_on('cmake', type='build')
    depends_on("qt")

    # VTK7 defaults to OpenGL2 rendering backend
    variant('opengl2', default=True,
            description='Build with OpenGL instead of OpenGL2 backend')
    variant('python', default=False,
            description='Build the python modules')

    def install(self, spec, prefix):
        def feature_to_bool(feature, on='ON', off='OFF'):
            if feature in spec:
                return on
            return off

        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-DBUILD_SHARED_LIBS=ON",
                "-DVTK_WRAP_PYTHON=" + ("ON" if "+python" in spec else "OFF"),
                # Disable wrappers for other languages.
                "-DVTK_WRAP_JAVA=OFF",
                "-DVTK_WRAP_TCL=OFF"]
            cmake_args.extend(std_cmake_args)

            # Enable Qt support here.
            cmake_args.extend([
                "-DQT_QMAKE_EXECUTABLE:PATH=%s/qmake" % spec['qt'].prefix.bin,
                "-DVTK_Group_Qt:BOOL=ON",
                # Ignore webkit because it's hard to build w/Qt
                "-DVTK_Group_Qt=OFF",
                "-DModule_vtkGUISupportQt:BOOL=ON",
                "-DModule_vtkGUISupportQtOpenGL:BOOL=ON"
            ])

            if spec['qt'].satisfies('@5'):
                cmake_args.append("-DVTK_QT_VERSION:STRING=5")

            if spec.satisfies("@6.1.0"):
                cmake_args.append("-DCMAKE_C_FLAGS=-DGLX_GLXEXT_LEGACY")
                cmake_args.append("-DCMAKE_CXX_FLAGS=-DGLX_GLXEXT_LEGACY")

            cmake_args.append('-DVTK_RENDERING_BACKEND:STRING=%s' %
                              feature_to_bool('+opengl2', 'OpenGL2', 'OpenGL'))

            cmake(*cmake_args)
            make()
            make("install")
