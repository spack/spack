# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCmake(PythonPackage):
    """CMake is an open-source, cross-platform family of tools designed to
    build, test and package software
    """

    homepage = "https://cmake.org/"
    pypi = "cmake/cmake-3.18.0.tar.gz"

    version('3.18.4', sha256='40b9a559e4e0dc43ff130a9df2272f495ad73844b395c2b01648efac3d69d34d')
    version('3.18.2', sha256='4570fbff976d8b920501c5e8f3c281e88bdad277bb14e0045dc051f319528656')
    version('3.18.0', sha256='52b98c5ee70b5fa30a8623e96482227e065292f78794eb085fdf0fecb204b79b')

    depends_on('cmake@3.18.0', type=('build', 'link', 'run'), when='@3.18.0')
    depends_on('py-scikit-build', type='build')
