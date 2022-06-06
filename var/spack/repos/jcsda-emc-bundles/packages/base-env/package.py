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

    maintainers = ['climbfuji', 'kgerheiser']

    version('main')
    version('1.0.0', preferred=True)

    with when('@main'):
        if sys.platform == 'darwin':
            depends_on('libbacktrace', type='run')
        depends_on('cmake', type='run')
        depends_on('curl', type='run')
        depends_on('git', type='run')
        depends_on('hdf5', type='run')
        depends_on('nccmp', type='run')
        depends_on('netcdf-c', type='run')
        depends_on('netcdf-fortran', type='run')
        depends_on('parallel-netcdf', type='run')
        depends_on('parallelio', type='run')
        depends_on('python@3.7:')
        depends_on('szip', type='run')
        depends_on('wget', type='run')
        depends_on('zlib', type='run')

    with when('@1.0.0'):
        if sys.platform == 'darwin':
            depends_on('libbacktrace', type='run')
        depends_on('cmake@3.21:', type='run')
        depends_on('curl', type='run')
        depends_on('git', type='run')
        depends_on('hdf5@1.12.1', type='run')
        depends_on('nccmp@1.9.0.1', type='run')
        depends_on('netcdf-c@4.8.1', type='run')
        depends_on('netcdf-fortran@4.5.4', type='run')
        depends_on('parallel-netcdf@1.12.2', type='run')
        depends_on('parallelio@2.5.4', type='run')
        depends_on('python@3.7:')
        depends_on('szip', type='run')
        depends_on('wget', type='run')
        depends_on('zlib@1.2.12', type='run')