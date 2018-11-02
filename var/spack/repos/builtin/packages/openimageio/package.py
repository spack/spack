# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openimageio(CMakePackage):
    """OpenImageIO is a library for reading and writing images, and a bunch of
    related classes, utilities, and applications."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.openimageio.org"
    url      = "https://github.com/OpenImageIO/oiio/archive/Release-1.8.15.tar.gz"

    version('1.8.15', sha256='4d5b4ed3f2daaed69989f53c0f9364dd87c82dc0a09807b5b6e9008e2426e86f')


    # Core dependencies
    depends_on('cmake@3.2.2:', type='build')
    depends_on('boost@1.53:', type=('build', 'link'))
    depends_on('libtiff@4.0:', type=('build', 'link'))
    depends_on('openexr@2.3:', type=('build', 'link'))
    depends_on('libpng@1.6:', type=('build', 'link'))

    # Optional dependencies
    variant('ffmpeg', default=False, description="Support video frames")
    depends_on('ffmpeg', when='+ffmpeg')

    variant('jpeg2k', default=False, description="Support for JPEG2000 format")
    depends_on('openjpeg', when='+jpeg2k')

    variant('python', default=False, description="Build python bindings")
    extends('python', when='+python')
    depends_on('numpy', when='+python')
    depends_on('py-pybind11', when='+python')

    variant('qt', default=False, description="Build qt viewer")
    depends_on('qt@5.6.0:+opengl', when='+qt')

    def cmake_args(self):
        args = ["-DUSE_FFMPEG={}".format('ON' if '+ffmpeg' in self.spec else 'OFF'),
                "-DUSE_OPENJPEG={}".format('ON' if '+jpeg2k' in self.spec else 'OFF'),
                "-DUSE_PYTHON={}".format('ON' if '+python' in self.spec else 'OFF'),
                "-DUSE_QT={}".format('ON' if '+qt' in self.spec else 'OFF')]
        return args
