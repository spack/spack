# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# -----------------------------------------------------------------------------
# Author: Derick Huth <derick.huth@utah.edu>
# -----------------------------------------------------------------------------
#   Note: This package was created by the ctop reaserch group at
#         the University of Utah, Shool of Computing and is unifiliated
#         with IEGenLib
# -----------------------------------------------------------------------------
from spack import *


class Iegenlib(Package):
    """Inspector/Executor Generation Library for manipulating sets
       and relations with uninterpreted function symbols. """

    homepage = "http://github.com/CompOpt4Apps"
    git      = "https://github.com/CompOpt4Apps/IEGenLib.git"

    version('master', branch='master')

    depends_on('cmake@2.6:', type='build')
    depends_on('isl')
    depends_on('texinfo', type='build')

    def install(self, spec, prefix):
        configure('--prefix', prefix)
        make()
        make('install')
