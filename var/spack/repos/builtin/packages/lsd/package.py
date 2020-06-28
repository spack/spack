# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lsd(CargoPackage):
    """
    LSD (LSDeluxe)

    The next gen ls command
    """

    homepage = "https://github.com/peltoche/lsd"
    crates_io = "lsd"
    git = "https://github.com/peltoche/lsd.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.17.0', sha256='d1e376b5db9c01304b4545f03d642ac5fa480289f060d014b1cec3a0df2c3990')
