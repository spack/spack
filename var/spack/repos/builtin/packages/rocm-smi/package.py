# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmSmi(MakefilePackage):
    """This tool exposes functionality for clock and temperature
       management of your ROCm enabled system"""

    homepage = "https://github.com/RadeonOpenCompute/ROC-smi"
    url      = "https://github.com/RadeonOpenCompute/ROC-smi/archive/rocm-3.7.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='4e34b3b4e409bb89677882f47d9988d56bc2d9bb9893f0712c22a4b73789e06a')
    version('3.5.0', sha256='4f46e947c415a4ac12b9f6989f15a42afe32551706b4f48476fba3abf92e8e7c')

    def install(self, spec, prefix):
        copy('rocm_smi.py', prefix)
        symlink('rocm_smi.py', join_path(prefix, 'rocm_smi'))
