##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Opencv(CMakePackage):
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

    version('master', git="https://github.com/opencv/opencv.git", branch="master")
    version('3.3.0',    '98a4e4c6f23ec725e808a891dc11eec4')
    version('3.2.0',    'a43b65488124ba33dde195fea9041b70')
    version('3.1.0',    '70e1dd07f0aa06606f1bc0e3fa15abd3')
    version('2.4.13.2', 'fe52791ce523681a67036def4c25261b')
    version('2.4.13.1', 'f6d354500d5013e60dc0fc44b07a63d1')
    version('2.4.13',   '8feb45a71adad89b8017a777477c3eff')
    version('2.4.12.3', '2496a4a4caf8fecfbfc294fbe6a814b0')
    version('2.4.12.2', 'bc0c60c2ea1cf4078deef99569912fc7')
    version('2.4.12.1', '7192f51434710904b5e3594872b897c3')

    # Standard variants
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('lapack', default=True, description='Include Lapack library support') # 3.3.0
    variant('powerpc', default=True, description='Enable PowerPC for GCC') # 2.4.13, 3.3.0
    variant('fast-math', default=False, description='Enable -ffast-math (not recommended for GCC 4.6.x)') # 2.4.13, 3.3.0

    # OpenCV modules
    variant('calib3d', default=True, description='calib3d module')
    variant('core', default=True, description='Include opencv_core module into the OpenCV build')
    variant('dnn', default=True, description='Build DNN support')
    variant('features2d', default=True, description='features2d module')
    variant('flann', default=True, description='flann module')
    variant('highgui', default=True, description='Include opencv_highgui module into the OpenCV build')
    variant('imgproc', default=True, description='Include opencv_imgproc module into the OpenCV build')
    variant('java', default=True,
            description='Activates support for Java')
    variant('ml', default=True, description='Build ML support')
    variant('python', default=True,
            description='Enables the build of Python extensions')
    variant('stitching', default=True, description='stitching module')
    variant('superres', default=True, description='superres module')
    variant('ts', default=True, description='Include opencv_ts module into the OpenCV build')
    variant('video', default=True, description='video module')
    variant('videostab', default=True, description='videostab module')
    variant('videoio', default=True, description='videoio module')

    # Optional 3rd party components
    variant('cuda', default=False, description='Activates support for CUDA')
    variant('eigen', default=True, description='Activates support for eigen')
    variant('ipp', default=True, description='Activates support for IPP')
    variant('ipp_iw', default=False, description='Build IPP IW from source')
    variant('jasper', default=True, description='Activates support for JasPer')
    variant('jpeg', default=False, description='Include JPEG support')
    variant('opencl', default=True, description='Include OpenCL Runtime support') # when='@2.4.13:')
    variant('opencl_svm', default=True, description='Include OpenCL Shared Virtual Memory support') #, when='@3.3.0:')
    variant('openclamdfft', default=True, description='Include OpenCL AMD OpenCL FFT library support') #, when='@2.4.13:')
    variant('openclamdblas', default=True, description='Include OpenCL AMD OpenCL BLAS library support') #, when='@2.4.13:')
    variant('openmp', default=False, description='Activates support for OpenMP threads')
    variant('pthreads_pf', default=True, description='Use pthreads-based parallel_for') # when='@3.3.0:'
    variant('png', default=False, description='Include PNG support')
    variant('qt', default=False, description='Activates support for QT')
    variant('gtk', default=False, description='Activates support for GTK')
    variant('tiff', default=False, description='Include TIFF support')
    variant('vtk', default=False, description='Activates support for VTK')
    variant('zlib', default=False, description='Build zlib from source')

    depends_on('eigen~mpfr', when='+eigen', type='build')

    depends_on('zlib', when='+zlib')
    depends_on('libpng', when='+png')
    depends_on('jpeg', when='+jpeg')
    depends_on('libtiff', when='+tiff')

    depends_on('jasper', when='+jasper')
    depends_on('cuda', when='+cuda')
    depends_on('gtkplus', when='+gtk')
    depends_on('vtk', when='+vtk')
    depends_on('qt', when='+qt')
    depends_on('java', when='+java')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('protobuf@3.1.0', when='@3.3.0: +dnn')

    depends_on('ffmpeg', when='+videoio')

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec

        # Standard variants
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format((
                'ON' if '+shared' in spec else 'OFF')),
            '-DENABLE_PRECOMPILED_HEADERS:BOOL=OFF',
            '-DWITH_LAPACK={0}'.format((
                'ON' if '+lapack' in spec else 'OFF')),
            '-DENABLE_POWERPC={0}'.format((
                'ON' if '+powerpc' in spec else 'OFF')),
            '-DENABLE_FAST_MATH={}'.format((
                'ON' if '+fast-math' in spec else 'OFF')),
        ]

        # modules
        args.extend([
            '-DBUILD_opencv_calib3d={0}'.format((
                'ON' if '+calib3d' in spec else 'OFF')),
            '-DBUILD_opencv_core:BOOL={0}'.format((
                'ON' if '+core' in spec else 'OFF')),
            '-DBUILD_opencv_dnn:BOOL={0}'.format((
                'ON' if '+dnn' in spec else 'OFF')),
            '-DBUILD_opencv_features2d={0}'.format((
                'ON' if '+features2d' in spec else 'OFF')),
            '-DBUILD_opencv_flann={0}'.format((
                'ON' if '+flann' in spec else 'OFF')),
            '-DBUILD_opencv_highgui:BOOL={0}'.format((
                'ON' if '+highgui' in spec else 'OFF')),
            '-DBUILD_opencv_imgproc:BOOL={0}'.format((
                'ON' if '+imgproc' in spec else 'OFF')),
            '-DBUILD_opencv_java:BOOL={0}'.format((
                'ON' if '+java' in spec else 'OFF')),
            '-DBUILD_opencv_ml={0}'.format((
                'ON' if '+ml' in spec else 'OFF')),
            '-DBUILD_opencv_stitching={0}'.format((
                'ON' if '+stitching' in spec else 'OFF')),
            '-DBUILD_opencv_superres={0}'.format((
                'ON' if '+superres' in spec else 'OFF')),
            '-DBUILD_opencv_ts={0}'.format((
                'ON' if '+ts' in spec else 'OFF')),
            '-DBUILD_opencv_video={0}'.format((
                'ON' if '+video' in spec else 'OFF')),
            '-DBUILD_opencv_videostab={0}'.format((
                'ON' if '+videostab' in spec else 'OFF')),
            '-DBUILD_opencv_videoio={0}'.format((
                'ON' if '+videoio' in spec else 'OFF')),
        ])

        # 3rd party components
        args.extend([
            '-DWITH_CUDA:BOOL={0}'.format((
                'ON' if '+cuda' in spec else 'OFF')),
            '-DWITH_EIGEN={0}'.format((
                'ON' if '+eigen' in spec else 'OFF')),
            '-DWITH_IPP:BOOL={0}'.format((
                'ON' if '+ipp' in spec else 'OFF')),
            '-DBUILD_IPP_IW:BOOL={0}'.format((
                'ON' if '+ipp_iw' in spec else 'OFF')),
            '-DWITH_JPEG:BOOL={0}'.format((
                'ON' if '+jpeg' in spec else 'OFF')),
            '-DWITH_OPENCL={0}'.format((
                'ON' if '+opencl' in spec else 'OFF')),
            '-DWITH_OPENCL_SVM={0}'.format((
                'ON' if '+opencl_svm' in spec else 'OFF')),
            '-DWITH_OPENCLAMDFFT={0}'.format((
                'ON' if '+openclamdfft' in spec else 'OFF')),
            '-DWITH_OPENCLAMDBLAS={0}'.format((
                'ON' if '+openclamdblas' in spec else 'OFF')),
            '-DWITH_OPENMP:BOOL={0}'.format((
                'ON' if '+openmp' in spec else 'OFF')),
            '-DWITH_PTHREADS_PF={0}'.format((
                'ON' if '+pthreads_pf' in spec else 'OFF')),
            '-DWITH_PNG:BOOL={0}'.format((
                'ON' if '+png' in spec else 'OFF')),
            '-DWITH_QT:BOOL={0}'.format((
                'ON' if '+qt' in spec else 'OFF')),
            '-DWITH_TIFF:BOOL={0}'.format((
                'ON' if '+tiff' in spec else 'OFF')),
            '-DWITH_VTK:BOOL={0}'.format((
                'ON' if '+vtk' in spec else 'OFF')),
            '-DWITH_ZLIB:BOOL={0}'.format((
                'ON' if '+zlib' in spec else 'OFF')),
        ])

        # Media I/O
        if '+zlib' in spec:
            zlib = spec['zlib']
            args.extend([
                '-DZLIB_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if '+debug' in spec else 'RELEASE'),
                    join_path(zlib.prefix.lib,
                              'libz.{0}'.format(dso_suffix))),
                '-DZLIB_INCLUDE_DIR:PATH={0}'.format(zlib.prefix.include)
            ])

        if '+png' in spec:
            libpng = spec['libpng']
            args.extend([
                '-DPNG_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if '+debug' in spec else 'RELEASE'),
                    join_path(libpng.prefix.lib,
                              'libpng.{0}'.format(dso_suffix))),
                '-DPNG_INCLUDE_DIR:PATH={0}'.format(libpng.prefix.include)
            ])

        if '+jpeg' in spec:
            libjpeg = spec['jpeg']
            args.extend([
                '-DBUILD_JPEG:BOOL=OFF',
                '-DJPEG_LIBRARY:FILEPATH={0}'.format(
                    join_path(libjpeg.prefix.lib,
                              'libjpeg.{0}'.format(dso_suffix))),
                '-DJPEG_INCLUDE_DIR:PATH={0}'.format(libjpeg.prefix.include)
            ])

        if '+tiff' in spec:
            libtiff = spec['libtiff']
            args.extend([
                '-DTIFF_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if '+debug' in spec else 'RELEASE'),
                    join_path(libtiff.prefix.lib,
                              'libtiff.{0}'.format(dso_suffix))),
                '-DTIFF_INCLUDE_DIR:PATH={0}'.format(libtiff.prefix.include)
            ])

        if '+jasper' in spec:
            jasper = spec['jasper']
            args.extend([
                '-DJASPER_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if '+debug' in spec else 'RELEASE'),
                    join_path(jasper.prefix.lib,
                              'libjasper.{0}'.format(dso_suffix))),
                '-DJASPER_INCLUDE_DIR:PATH={0}'.format(jasper.prefix.include)
            ])

        # GUI
        if '+gtk' not in spec:
            args.extend([
                '-DWITH_GTK:BOOL=OFF',
                '-DWITH_GTK_2_X:BOOL=OFF'
            ])
        elif '^gtkplus@3:' in spec:
            args.extend([
                '-DWITH_GTK:BOOL=ON',
                '-DWITH_GTK_2_X:BOOL=OFF'
            ])
        elif '^gtkplus@2:3' in spec:
            args.extend([
                '-DWITH_GTK:BOOL=OFF',
                '-DWITH_GTK_2_X:BOOL=ON'
            ])

        # Python
        if '+python' in spec:
            python_exe = spec['python'].command.path
            python_lib = spec['python'].libs[0]
            python_include_dir = spec['python'].headers.directories[0]

            if '^python@3:' in spec:
                args.extend([
                    '-DBUILD_opencv_python3=ON',
                    '-DPYTHON3_EXECUTABLE={0}'.format(python_exe),
                    '-DPYTHON3_LIBRARY={0}'.format(python_lib),
                    '-DPYTHON3_INCLUDE_DIR={0}'.format(python_include_dir),
                    '-DBUILD_opencv_python2=OFF',
                ])
            elif '^python@2:3' in spec:
                args.extend([
                    '-DBUILD_opencv_python2=ON',
                    '-DPYTHON2_EXECUTABLE={0}'.format(python_exe),
                    '-DPYTHON2_LIBRARY={0}'.format(python_lib),
                    '-DPYTHON2_INCLUDE_DIR={0}'.format(python_include_dir),
                    '-DBUILD_opencv_python3=OFF',
                ])
        else:
            args.extend([
                '-DBUILD_opencv_python2=OFF',
                '-DBUILD_opencv_python3=OFF'
            ])

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            "libopencv_*", root=self.prefix, shared=shared, recurse=True
        )
