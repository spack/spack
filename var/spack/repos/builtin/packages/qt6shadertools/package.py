# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Qt6shadertools(CMakePackage):
    """APIs and tools in this module provide the producer functionality for the
    shader pipeline that allows Qt Quick to operate on Vulkan, Metal, and
    Direct3D, in addition to OpenGL."""

    url      = "https://github.com/qt/qtshadertools/archive/refs/tags/v6.2.3.tar.gz"

    maintainers = ['wdconinc', 'sethrj']

    version('6.2.3', sha256='658c4acc2925e57d35bbd38cdf49c08297555ed7d632f9e86bfef76e6d861562')

    generator = 'Ninja'

    # Changing default to Release for typical use in HPC contexts
    variant('build_type',
            default='Release',
            values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
            description='CMake build type')

    depends_on('cmake@3.16:', type='build')
    depends_on('ninja', type='build')
    depends_on("pkgconfig", type='build')
    depends_on("python", when='@5.7.0:', type='build')

    versions = ['6.2.3']
    for v in versions:
        depends_on('qt6base@{}'.format(v), when='@{}'.format(v))

    def patch(self):
        import shutil
        vendor_dir = join_path(self.stage.source_path, 'src/3rdparty')
        vendor_deps_to_keep = ['glslang', 'patches', 'SPIRV-Cross']
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep not in vendor_deps_to_keep:
                        shutil.rmtree(dep)

    def cmake_args(self):
        args = []
        return args
