# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyCmake(PythonPackage):
    """CMake is an open-source, cross-platform family of tools designed to
    build, test and package software
    """

    homepage = "https://cmake.org"
    git = "https://github.com/scikit-build/cmake-python-distributions.git"
    pypi = "cmake/cmake-3.22.2.tar.gz"

    version('3.22.2', sha256='b5bd5eeb488b13cf64ec963800f3d979eaeb90b4382861b86909df503379e219')
    version('3.21.4', sha256='30fa5ed8a5ad66dcd263adb87f3ce3dc2d0ec0ac3958f5becff577e4b62cd065')
    version('3.18.0', sha256='52b98c5ee70b5fa30a8623e96482227e065292f78794eb085fdf0fecb204b79b')

    depends_on('ninja', type='build')
    depends_on('py-scikit-build@0.12:', type='build')
    depends_on('py-setuptools@42:', type='build')
    depends_on('git', type='build')
    depends_on('cmake@3.22.2', type=('build', 'link', 'run'), when='@3.22.2')
    depends_on('cmake@3.21.4', type=('build', 'link', 'run'), when='@3.21.4')
    depends_on('cmake@3.18.0', type=('build', 'link', 'run'), when='@3.18.0')

    # see:
    #   https://github.com/scikit-build/cmake-python-distributions/issues/227
    #   https://github.com/spack/spack/pull/28760#issuecomment-1029362288
    for v in ['3.22.2', '3.21.4', '3.18.0']:
        resource(name='cmake-src',
                 git='https://gitlab.kitware.com/cmake/cmake.git',
                 commit='v{0}'.format(v), when='@{0}'.format(v),
                 destination='cmake-src', placement='cmake-src')

    def install_options(self, spec, prefix):
        return [
            '-DBUILD_CMAKE_FROM_SOURCE=ON',
            '-DCMakeProject_SOURCE_DIR=cmake-src'
        ]
