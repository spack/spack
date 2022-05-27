# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PreferredTest(Package):
    """Dummy package with develop version and preferred version"""
    homepage = "https://github.com/LLNL/mpileaks"
    url      = "https://github.com/LLNL/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

    version('develop', git='https://github.com/LLNL/mpileaks.git')
    version('1.0', sha256='2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825', preferred=True)
