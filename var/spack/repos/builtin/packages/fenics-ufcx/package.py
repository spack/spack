# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsUfcx(CMakePackage):
    """FFCx provides the ufcx.h interface header for finite element kernels,
       used by DOLFINx. ufcx.h can be installed from the FFCx repo without
       making it dependent on Python.
    """

    homepage = 'https://github.com/FEniCS/ffcx'
    git = 'https://github.com/FEniCS/ffcx.git'
    url = 'https://github.com/FEniCS/ffcx/archive/v0.4.0.tar.gz'
    maintainers = ['ma595']

    version('main', branch='main')
    version('0.4.0', sha256='2145286576304cf303f2c94dbea3bd7de0d2140797202d9504c0d581eea9cbc1')

    root_cmakelists_dir = 'cmake'
