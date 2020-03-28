# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gdrcopy(MakefilePackage):
    """A fast GPU memory copy library based on NVIDIA GPUDirect
       RDMA technology."""

    homepage = "https://github.com/NVIDIA/gdrcopy"
    url      = "https://github.com/NVIDIA/gdrcopy/archive/v2.0-beta.3.tar.gz"
    git      = "https://github.com/NVIDIA/gdrcopy"

    version('master', branch='master')
    version('2.0', sha256='98320e6e980a7134ebc4eedd6cf23647104f2b3c557f2eaf0d31a02609f5f2b0')
    version('1.3', sha256='f11cdfe389b685f6636b80b4a3312dc014a385ad7220179c1318c60e2e28af3a')

    def build(self, spec, prefix):
        make('lib')

    def install(self, spec, prefix):
        mkdir(prefix.include)
        mkdir(prefix.lib64)
        make('lib_install', 'PREFIX={0}'.format(self.prefix))
