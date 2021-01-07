# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Genfit(CMakePackage):
    """GenFit is a tracking framework in particle and nuclear physics."""

    homepage = "https://github.com/GenFit/GenFit"
    url      = "https://github.com/GenFit/GenFit/archive/master.zip"
    git      = "https://github.com/GenFit/GenFit.git"

    maintainers = ['mirguest']

    version('master', branch='master')

    depends_on('root')
