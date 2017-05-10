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


class Pcl(CMakePackage):
    """The Point Cloud Library (PCL) is a standalone, large scale, open
    project for 2D/3D image and point cloud processing.
    """

    homepage = "http://www.pointclouds.org/"
    url      = "https://github.com/PointCloudLibrary/pcl/archive/pcl-1.8.0.tar.gz"

    version('1.8.0',      '8c1308be2c13106e237e4a4204a32cca')
    version('1.7.2',      '02c72eb6760fcb1f2e359ad8871b9968')
    version('1.7.1',      'ce8fa17662544eb4bb7b084191a61ad5')
    version('1.7.0',      'e2ac2d2e72825d991c6d194f9586b5d8')

    variant("usb",    default=False,
            description="Build USB RGBD-Camera drivers.")
    variant("png",    default=True,
            description="PNG file support.")
    variant("qhull",  default=True,
            description="Include convex-hull operations.")
    variant("cuda",   default=False,
            description="Build NVIDIA-CUDA support.")
    variant("qt",     default=False,
            description="Build QT Front-End. Qt4 or Qt5 required.")
    variant("vtk",    default=False,
            description="Build VTK-Visualizations.")
    variant("opengl", default=False,
            description="Support for OpenGL.")
    variant("pcap",   default=False,
            description="pcap file capabilities in Velodyne HDL driver.")

    conflicts("~opengl", when="+qt")
    conflicts("~opengl", when="+vtk")
    conflicts("~qt",     when="+vtk")  # vtk depends on qt, use it
    conflicts("~opengl", when="+cuda")

    # Dependencies as discerned from here:
    # http://pointclouds.org/documentation/tutorials/compiling_pcl_posix.php
    depends_on('pkg-config')
    # TODO: how to give boost version AND specific boost library
    # requirements? What should they be / variants can't embed optional
    # boost deps right?
    #
    # REQUIRED boost:
    #     If OpenNI2: +system+filesystem+thread+date_time+iostreams+chrono
    #     Else:       +system+filesystem+thread+date_time+iostreams
    # OPTIONAL boost:
    #     +serialization+mpi
    #
    # Reference:
    #
    depends_on('boost@1.47.0:')
    depends_on('eigen@3.0.0:')
    depends_on('flann@1.7.0:')

    depends_on("metis")   # unmentioned, they vendor in 3rd party if not found.

    # TODO:
    # What to do about python?  It depends on opencv+python, but they are
    # some kind of extension, and install underneath opencv?
    # https://github.com/PointCloudLibrary/pcl/blob/6f846d242b07b7b2d5a562bbc60b3b488bbf6a47/cmake/pcl_find_python.cmake
    # There is also a python-pcl package they maintain?
    # http://pointclouds.org/news/tags/python

    depends_on("libusb",  when="+usb")
    depends_on("libpng",  when="+png")
    depends_on("qhull",   when="+qhull")
    depends_on("cuda",    when="+cuda")
    depends_on("qt@4:",   when="+qt")
    depends_on("vtk",     when="+vtk")
    depends_on("libpcap", when="+pcap")

    # TODO: should something be done with the default options?
    # https://github.com/PointCloudLibrary/pcl/blob/master/cmake/pcl_options.cmake

    # TODO: spack will never be suited to nor should attempt to be suited
    # to install RGBD camera drivers.  How should spack inform users to
    # be sure that they are going to get what they want?
    #
    # The drivers require elevated permissions, and most often custom
    # modules and startup scripts.  The user is advised to try and
    # install from the official SDK or their system package manager
    # where possible.
    #
    # NOTE: libusb support REQUIRED for ANY to be used.
    #
    # Currently, the available driver support that can be built:
    # https://github.com/PointCloudLibrary/pcl/blob/b9022ebd8ad5f5300662069b5f79995d0c0e18be/CMakeLists.txt#L296-L303
    #
    # The way it works is that everything is default to TRUE, the library
    # is attempted to be found, and if not ignored.
    #
    # It takes place here:
    # https://github.com/PointCloudLibrary/pcl/blob/b89b32b5e812353e93a5c35203c70b878c8ae2b7/cmake/pcl_targets.cmake#L842-L864

    def cmake_args(self):
        args = []
        spec = self.spec

        usb_support = "ON" if "+usb" in spec else "OFF"
        args.append("-DWITH_LIBUSB:BOOL={0}".format(usb_support))

        png_support = "ON" if "+png" in spec else "OFF"
        args.append("-DWITH_PNG:BOOL={0}".format(png_support))

        with_qhull = "ON" if "+qhull" in spec else "OFF"
        args.append("-DWITH_QHULL:BOOL={0}".format(with_qhull))

        with_cuda = "ON" if "+cuda" in spec else "OFF"
        args.append("-DWITH_CUDA:BOOL={0}".format(with_cuda))

        using_qt = "+qt" in spec
        with_qt = "ON" if using_qt else "OFF"
        args.append("-DWITH_QT:BOOL={0}".format(with_qt))
        if using_qt:
            # TODO: how do i check this?
            if self.spec.satisfies("^qt@4.8.6"):
                qt_ver_str = "4"
            else:
                qt_ver_str = "5"
            args.append("-DPCL_QT_VERSION:STRING={0}".format(qt_ver_str))

        with_vtk = "ON" if "+vtk" in spec else "OFF"
        args.append("-DWITH_VTK:BOOL={0}".format(with_vtk))

        with_pcap = "ON" if "+pcap" in spec else "OFF"
        args.append("-DWITH_PCAP:BOOL={0}".format(with_pcap))

        with_opengl = "ON" if "+opengl" in spec else "OFF"
        args.append("-DWITH_OPENGL:BOOL={0}".format(with_opengl))

        return args
