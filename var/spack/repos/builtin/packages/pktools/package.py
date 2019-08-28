# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pktools(CMakePackage):
    """Processing Kernel for geospatial data"""

    homepage = "http://pktools.nongnu.org/html/index.html"
    url      = "http://download.savannah.gnu.org/releases/pktools/pktools-2.6.7.tar.gz"

    version('2.6.7.1', sha256='519b6a500ce3c5ef3793c1cda1f5377f13b7d7591b5ccc376b2bd1de4bd4f7e5')
    version('2.6.7',   sha256='f566647e93037cc01cebfe17ea554d798177fe5081887c70223dcca817f4fe7f')

    depends_on('gdal')
    depends_on('gsl')
    depends_on('armadillo')
    depends_on('nlopt')
    depends_on('boost')
    depends_on('fann')

    def cmake_args(self):
        args = []
        # liblas is not avaialable in spack yet
        # On Centos7, build fails with system liblas
        args.append('-DBUILD_WITH_LIBLAS=OFF')
        args.append('-DCMAKE_CXX_STANDARD=11')
        args.append('-DPKTOOLS_WITH_UTILITIES=ON')
        args.append('-DBUILD_WITH_FANN=ON')
        return args
