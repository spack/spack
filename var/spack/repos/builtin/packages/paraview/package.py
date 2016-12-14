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


class Paraview(Package):
    homepage = 'http://www.paraview.org'
    url      = 'http://www.paraview.org/files/v5.0/ParaView-v'
    _url_str = 'http://www.paraview.org/files/v%s/ParaView-v%s-source.tar.gz'

    version('4.4.0', 'fa1569857dd680ebb4d7ff89c2227378')
    version('5.0.0', '4598f0b421460c8bbc635c9a1c3bdbee')

    variant('python', default=False, description='Enable Python support')

    variant('tcl', default=False, description='Enable TCL support')

    variant('mpi', default=True, description='Enable MPI support')

    variant('osmesa', default=False, description='Enable OSMesa support')
    variant('qt', default=False, description='Enable Qt support')
    variant('opengl2', default=False, description='Enable OpenGL2 backend')

    depends_on('python@2:2.7', when='+python')
    depends_on('py-numpy', when='+python', type='run')
    depends_on('py-matplotlib', when='+python', type='run')
    depends_on('tcl', when='+tcl')
    depends_on('mpi', when='+mpi')
    depends_on('qt@:4', when='+qt')

    depends_on('cmake', type='build')
    depends_on('bzip2')
    depends_on('freetype')
    # depends_on('hdf5+mpi', when='+mpi')
    # depends_on('hdf5~mpi', when='~mpi')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    # depends_on('netcdf')
    # depends_on('netcdf-cxx')
    # depends_on('protobuf') # version mismatches?
    # depends_on('sqlite') # external version not supported
    depends_on('zlib')

    def url_for_version(self, version):
        """Handle ParaView version-based custom URLs."""
        return self._url_str % (version.up_to(2), version)

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            def feature_to_bool(feature, on='ON', off='OFF'):
                if feature in spec:
                    return on
                return off

            def nfeature_to_bool(feature):
                return feature_to_bool(feature, on='OFF', off='ON')

            feature_args = std_cmake_args[:]
            feature_args.append(
                '-DPARAVIEW_BUILD_QT_GUI:BOOL=%s' % feature_to_bool('+qt'))
            feature_args.append('-DPARAVIEW_ENABLE_PYTHON:BOOL=%s' %
                                feature_to_bool('+python'))
            if '+python' in spec:
                feature_args.append(
                    '-DPYTHON_EXECUTABLE:FILEPATH=%s/bin/python'
                    % spec['python'].prefix)
            feature_args.append('-DPARAVIEW_USE_MPI:BOOL=%s' %
                                feature_to_bool('+mpi'))
            if '+mpi' in spec:
                feature_args.append(
                    '-DMPIEXEC:FILEPATH=%s/bin/mpiexec' % spec['mpi'].prefix)
            feature_args.append(
                '-DVTK_ENABLE_TCL_WRAPPING:BOOL=%s' % feature_to_bool('+tcl'))
            feature_args.append('-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' %
                                feature_to_bool('+osmesa'))
            feature_args.append('-DVTK_USE_X:BOOL=%s' %
                                nfeature_to_bool('+osmesa'))
            feature_args.append(
                '-DVTK_RENDERING_BACKEND:STRING=%s' %
                feature_to_bool('+opengl2', 'OpenGL2', 'OpenGL'))

            feature_args.extend(std_cmake_args)

            if 'darwin' in self.spec.architecture:
                feature_args.append('-DVTK_USE_X:BOOL=OFF')
                feature_args.append(
                    '-DPARAVIEW_DO_UNIX_STYLE_INSTALLS:BOOL=ON')

            cmake('..',
                  '-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix,
                  '-DBUILD_TESTING:BOOL=OFF',
                  '-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON',
                  '-DVTK_USE_SYSTEM_HDF5:BOOL=OFF',
                  '-DVTK_USE_SYSTEM_JPEG:BOOL=ON',
                  '-DVTK_USE_SYSTEM_LIBXML2:BOOL=ON',
                  '-DVTK_USE_SYSTEM_NETCDF:BOOL=OFF',
                  '-DVTK_USE_SYSTEM_TIFF:BOOL=ON',
                  '-DVTK_USE_SYSTEM_ZLIB:BOOL=ON',
                  *feature_args)
            make()
            make('install')
