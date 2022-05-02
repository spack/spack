# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class BaseEnv(BundlePackage):
    """Basic development environment used by other environments"""

    homepage = "https://github.com/noaa-emc/spack-stack"
    git      = "https://github.com/noaa-emc/spack-stack.git"

    maintainers = ['climbfuji', 'kgerheiser', 'rhoneyager']

    version('main', branch='main')

    # Basic utilities
    if sys.platform == 'darwin':
        depends_on('libbacktrace', type='run')
    depends_on('cmake', type='run')
    depends_on('git', type='run')
    depends_on('wget', type='run')
    depends_on('curl', type='run')

    # I/O
    depends_on('zlib', type='run')
    depends_on('szip', type='run')
    depends_on('hdf5', type='run')
    depends_on('netcdf-c', type='run')
    depends_on('netcdf-fortran', type='run')
    depends_on('parallel-netcdf', type='run')
    depends_on('parallelio', type='run')
    depends_on('nccmp', type='run')

    # Python
    depends_on('python@3.7:')
