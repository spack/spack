# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nvtop(CMakePackage):
    """NVIDIA GPUs htop like monitoring tool

       NOTE: to use this application you must have an NVIDIA display driver
       installed. (one which provides libnvidia-ml.so.1)"""

    homepage = "https://github.com/Syllo/nvtop"
    git      = "https://github.com/Syllo/nvtop.git"

    version('20190210', branch='dev', commit='453f025c0fda36708d03b85af9b39effcc170cd7')

    depends_on('cuda', type=('build', 'link', 'run'))

    def cmake_args(self):
        return ['-DNVML_LIBRARIES=%s' % self.get_nvml_lib]
