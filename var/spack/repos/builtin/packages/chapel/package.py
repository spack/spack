# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Chapel(AutotoolsPackage):
    """Chapel is a modern programming language that is parallel, productive,
       portable, scalable and open-source."""

    homepage = "https://chapel-lang.org/"
    url      = "https://github.com/chapel-lang/chapel/releases/download/1.24.1/chapel-1.24.1.tar.gz"

    version('1.24.1', sha256='f898f266fccaa34d937b38730a361d42efb20753ba43a95e5682816e008ce5e4')
    version('1.24.0', sha256='77c6087f3e0837268470915f2ad260d49cf7ac4adf16f5b44862ae624c1be801')
    version('1.23.0', sha256='7ae2c8f17a7b98ac68378e94a842cf16d4ab0bcfeabc0fee5ab4aaa07b205661')
    version('1.22.1', sha256='8235eb0869c9b04256f2e5ce3ac4f9eff558401582fba0eba05f254449a24989')
    version('1.22.0', sha256='57ba6ee5dfc36efcd66854ecb4307e1c054700ea201eff73012bd8b4572c2ce6')
    version('1.21.0', sha256='886f7ba0e0e86c86dba99417e3165f90b1d3eca59c8cd5a7f645ce28cb5d82a0')
    version('1.20.0', sha256='08bc86df13e4ad56d0447f52628b0f8e36b0476db4e19a90eeb2bd5f260baece')
    version('1.19.0', sha256='c2b68a20d87cc382c2f73dd1ecc6a4f42fb2f590b0b10fbc577382dd35c9e9bd')
    version('1.18.0', sha256='68471e1f398b074edcc28cae0be26a481078adc3edea4df663f01c6bd3b6ae0d')
