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
from glob import glob


class Opencv(Package):
    """OpenCV is released under a BSD license and hence it's free for both
    academic and commercial use. It has C++, C, Python and Java interfaces and
    supports Windows, Linux, Mac OS, iOS and Android. OpenCV was designed for
    computational efficiency and with a strong focus on real-time applications.
    Written in optimized C/C++, the library can take advantage of multi-core
    processing. Enabled with OpenCL, it can take advantage of the hardware
    acceleration of the underlying heterogeneous compute platform. Adopted all
    around the world, OpenCV has more than 47 thousand people of user community
    and estimated number of downloads exceeding 9 million. Usage ranges from
    interactive art, to mines inspection, stitching maps on the web or through
    advanced robotics.
    """

    homepage = 'http://opencv.org/'
    url = 'https://github.com/Itseez/opencv/archive/3.1.0.tar.gz'

    version('3.1.0', '70e1dd07f0aa06606f1bc0e3fa15abd3')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('debug', default=False,
            description='Builds a debug version of the libraries')

    variant('eigen', default=True, description='Activates support for eigen')
    variant('ipp', default=True, description='Activates support for IPP')
    variant('jasper', default=True, description='Activates support for JasPer')
    variant('cuda', default=False, description='Activates support for CUDA')
    variant('gtk', default=False, description='Activates support for GTK')
    variant('vtk', default=False, description='Activates support for VTK')
    variant('qt', default=False, description='Activates support for QT')
    variant('python', default=False,
            description='Enables the build of Python extensions')
    variant('java', default=False,
            description='Activates support for Java')

    depends_on('cmake', type='build')
    depends_on('eigen', when='+eigen', type='build')

    depends_on('zlib')
    depends_on('libpng')
    depends_on('libjpeg-turbo')
    depends_on('libtiff')

    depends_on('jasper', when='+jasper')
    depends_on('cuda', when='+cuda')
    depends_on('gtkplus', when='+gtk')
    depends_on('vtk', when='+vtk')
    depends_on('qt', when='+qt')
    depends_on('jdk', when='+java')
    depends_on('py-numpy', when='+python', type=('build', 'run'))

    extends('python', when='+python')

    def install(self, spec, prefix):
        cmake_options = []
        cmake_options.extend(std_cmake_args)

        cmake_options.extend([
            '-DCMAKE_BUILD_TYPE:STRING={0}'.format((
                'Debug' if '+debug' in spec else 'Release')),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format((
                'ON' if '+shared' in spec else 'OFF')),
            '-DENABLE_PRECOMPILED_HEADERS:BOOL=OFF',
            '-DWITH_IPP:BOOL={0}'.format((
                'ON' if '+ipp' in spec else 'OFF')),
            '-DWITH_CUDA:BOOL={0}'.format((
                'ON' if '+cuda' in spec else 'OFF')),
            '-DWITH_QT:BOOL={0}'.format((
                'ON' if '+qt' in spec else 'OFF')),
            '-DWITH_VTK:BOOL={0}'.format((
                'ON' if '+vtk' in spec else 'OFF')),
            '-DBUILD_opencv_java:BOOL={0}'.format((
                'ON' if '+java' in spec else 'OFF')),
        ])

        # Media I/O
        zlib = spec['zlib']
        cmake_options.extend([
            '-DZLIB_LIBRARY_{0}:FILEPATH={1}'.format((
                'DEBUG' if '+debug' in spec else 'RELEASE'),
                join_path(zlib.prefix.lib,
                          'libz.{0}'.format(dso_suffix))),
            '-DZLIB_INCLUDE_DIR:PATH={0}'.format(zlib.prefix.include)
        ])

        libpng = spec['libpng']
        cmake_options.extend([
            '-DPNG_LIBRARY_{0}:FILEPATH={1}'.format((
                'DEBUG' if '+debug' in spec else 'RELEASE'),
                join_path(libpng.prefix.lib,
                          'libpng.{0}'.format(dso_suffix))),
            '-DPNG_INCLUDE_DIR:PATH={0}'.format(libpng.prefix.include)
        ])

        libjpeg = spec['libjpeg-turbo']
        cmake_options.extend([
            '-DJPEG_LIBRARY:FILEPATH={0}'.format(
                join_path(libjpeg.prefix.lib,
                          'libjpeg.{0}'.format(dso_suffix))),
            '-DJPEG_INCLUDE_DIR:PATH={0}'.format(libjpeg.prefix.include)
        ])

        libtiff = spec['libtiff']
        cmake_options.extend([
            '-DTIFF_LIBRARY_{0}:FILEPATH={1}'.format((
                'DEBUG' if '+debug' in spec else 'RELEASE'),
                join_path(libtiff.prefix.lib,
                          'libtiff.{0}'.format(dso_suffix))),
            '-DTIFF_INCLUDE_DIR:PATH={0}'.format(libtiff.prefix.include)
        ])

        jasper = spec['jasper']
        cmake_options.extend([
            '-DJASPER_LIBRARY_{0}:FILEPATH={1}'.format((
                'DEBUG' if '+debug' in spec else 'RELEASE'),
                join_path(jasper.prefix.lib,
                          'libjasper.{0}'.format(dso_suffix))),
            '-DJASPER_INCLUDE_DIR:PATH={0}'.format(jasper.prefix.include)
        ])

        # GUI
        if '+gtk' not in spec:
            cmake_options.extend([
                '-DWITH_GTK:BOOL=OFF',
                '-DWITH_GTK_2_X:BOOL=OFF'
            ])
        elif '^gtkplus@3:' in spec:
            cmake_options.extend([
                '-DWITH_GTK:BOOL=ON',
                '-DWITH_GTK_2_X:BOOL=OFF'
            ])
        elif '^gtkplus@2:3' in spec:
            cmake_options.extend([
                '-DWITH_GTK:BOOL=OFF',
                '-DWITH_GTK_2_X:BOOL=ON'
            ])

        # Python
        if '+python' in spec:
            python = spec['python']

            try:
                python_lib = glob(join_path(
                    python.prefix.lib, 'libpython*.{0}'.format(dso_suffix)))[0]
            except KeyError:
                raise InstallError('Cannot find libpython')

            try:
                python_include_dir = glob(join_path(python.prefix.include,
                                                    'python*'))[0]
            except KeyError:
                raise InstallError('Cannot find python include directory')

            if '^python@3:' in spec:
                python_exe = join_path(python.prefix.bin, 'python3')
                cmake_options.extend([
                    '-DBUILD_opencv_python3=ON',
                    '-DPYTHON3_EXECUTABLE={0}'.format(python_exe),
                    '-DPYTHON3_LIBRARY={0}'.format(python_lib),
                    '-DPYTHON3_INCLUDE_DIR={0}'.format(python_include_dir),
                    '-DBUILD_opencv_python2=OFF',
                ])
            elif '^python@2:3' in spec:
                python_exe = join_path(python.prefix.bin, 'python2')
                cmake_options.extend([
                    '-DBUILD_opencv_python2=ON',
                    '-DPYTHON2_EXECUTABLE={0}'.format(python_exe),
                    '-DPYTHON2_LIBRARY={0}'.format(python_lib),
                    '-DPYTHON2_INCLUDE_DIR={0}'.format(python_include_dir),
                    '-DBUILD_opencv_python3=OFF',
                ])
        else:
            cmake_options.extend([
                '-DBUILD_opencv_python2=OFF',
                '-DBUILD_opencv_python3=OFF'
            ])

        with working_dir('spack_build', create=True):
            cmake('..', *cmake_options)
            make('VERBOSE=1')
            make("install")
