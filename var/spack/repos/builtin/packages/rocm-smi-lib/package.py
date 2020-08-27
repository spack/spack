# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import shutil


class RocmSmiLib(CMakePackage):
    """It is a C library for Linux that provides a user space interface
       for applications to monitor and control GPU applications."""

    homepage = "https://github.com/RadeonOpenCompute/rocm_smi_lib"
    url      = "https://github.com/RadeonOpenCompute/rocm_smi_lib/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='a5d2ec3570d018b60524f0e589c4917f03d26578443f94bde27a170c7bb21e6e')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    depends_on('cmake@3:', type='build')

    @run_after('install')
    def post_install(self):
        shutil.rmtree(self.prefix.lib)
        install_tree(self.prefix.rocm_smi,  self.prefix)
        shutil.rmtree(self.prefix.rocm_smi)
