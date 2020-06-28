# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sd(CargoPackage):
    """An intuitive find & replace CLI"""

    homepage  = "https://github.com/chmln/sd"
    crates_io = "sd"
    git       = "https://github.com/chmln/sd.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.7.5', sha256='ebd2d98ccd28280977baadbd41347de7a8edcaa95b052e04188b24a63341ec0d')
