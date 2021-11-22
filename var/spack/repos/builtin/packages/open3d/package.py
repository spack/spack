# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Open3d(CMakePackage, CudaPackage):
    """Open3D: A Modern Library for 3D Data Processing."""

    homepage = "http://www.open3d.org/"
    url      = "https://github.com/isl-org/Open3D/archive/refs/tags/v0.13.0.tar.gz"

    version('0.13.0', sha256='b5994a9853f1c01e59f6d682ef0cc42c73071fd49c3e30593dc2f21ec61cf940')

    variant('python', default=False, description='Build the Python module')

    # http://www.open3d.org/docs/latest/compilation.html
    depends_on('cmake@3.19:', type='build')
    depends_on('cuda@10.1:', when='+cuda')
    depends_on('eigen')
    depends_on('flann')
    depends_on('fmt')
    depends_on('glew')
    depends_on('glfw')
    depends_on('googletest')
    depends_on('imgui')
    depends_on('jpeg')
    depends_on('liblzf')
    depends_on('libpng')
    depends_on('py-pybind11')
    depends_on('qhull')
    depends_on('tinygltf')
    depends_on('tinyobjloader')

    # C++14 compiler required
    conflicts('%gcc@:4')
    conflicts('%clang@:6')

    def patch(self):
        # Force Python libraries to be installed to self.prefix
        filter_file('pip install', 'pip install --prefix ' + self.prefix,
                    os.path.join('cpp', 'pybind', 'make_install_pip_package.cmake'))

    def cmake_args(self):
        return [
            self.define_from_variant('BUILD_PYTHON_MODULE', 'python'),
            self.define_from_variant('BUILD_CUDA_MODULE', 'cuda'),
            # Use Spack-installed dependencies instead of vendored dependencies
            self.define('USE_SYSTEM_EIGEN3', True),
            self.define('USE_SYSTEM_FLANN', True),
            self.define('USE_SYSTEM_FMT', True),
            self.define('USE_SYSTEM_GLEW', True),
            self.define('USE_SYSTEM_GLFW', True),
            self.define('USE_SYSTEM_GOOGLETEST', True),
            self.define('USE_SYSTEM_IMGUI', True),
            self.define('USE_SYSTEM_JPEG', True),
            self.define('USE_SYSTEM_LIBLZF', True),
            self.define('USE_SYSTEM_PNG', True),
            self.define('USE_SYSTEM_PYBIND11', True),
            self.define('USE_SYSTEM_QHULL', True),
            self.define('USE_SYSTEM_TINYGLTF', True),
            self.define('USE_SYSTEM_TINYOBJLOADER', True),
        ]
