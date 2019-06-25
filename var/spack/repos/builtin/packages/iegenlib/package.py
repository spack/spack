# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Iegenlib(AutotoolsPackage):
    """Inspector/Executor Generation Library for manipulating sets
       and relations with uninterpreted function symbols. """

    homepage = "http://github.com/CompOpt4Apps"
    git      = "https://github.com/CompOpt4Apps/IEGenLib.git"

    maintainers = ['dhuth']

    version('master', branch='master')

    depends_on('cmake@2.6:', type='build')
    depends_on('isl')
    depends_on('texinfo', type='build')
