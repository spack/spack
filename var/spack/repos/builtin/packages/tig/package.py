# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tig(AutotoolsPackage):
    """Text-mode interface for git"""

    homepage = "https://jonas.github.io/tig/"
    url      = "https://github.com/jonas/tig/releases/download/tig-2.2.2/tig-2.2.2.tar.gz"

    version('2.2.2', '3b4a9f0fd8d18c1039863e6c4ace6e46')

    depends_on('ncurses')
