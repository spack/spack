# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DuDust(CargoPackage):
    """A more intuitive version of du"""

    homepage  = "https://github.com/bootandy/dust"
    crates_io = "du-dust"
    git       = "https://github.com/bootandy/dust.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.5.1', sha256='ddfcace4556c7318114307915452698c0aec64465f982c5cac0cdae01630b7a4')
