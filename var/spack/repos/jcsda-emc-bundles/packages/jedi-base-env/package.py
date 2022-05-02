# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediBaseEnv(BundlePackage):
    """Basic development environment for JEDI applications"""

    # Todo: update URL
    homepage = "https://github.com/JCSDA-internal/jedi-stack"
    git      = "https://github.com/JCSDA-internal/jedi-stack.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')

    depends_on('base-env', type='run')

    depends_on('bison', type='run')
    depends_on('flex', type='run')

    depends_on('netcdf-cxx4', type='run')

    depends_on('ecbuild', type='run')
    depends_on('jedi-cmake', type='run')

    depends_on('git-lfs', type='run')

    depends_on('eigen', type='run')
    depends_on('fftw-api', type='run')
    depends_on('gsl-lite', type='run')
    depends_on('udunits', type='run')

    depends_on('boost', type='run')
    depends_on('blas',  type='run')
    depends_on('eckit', type='run')
    depends_on('fckit', type='run')
    depends_on('atlas', type='run')
    depends_on('nlohmann-json', type='run')
    depends_on('nlohmann-json-schema-validator', type='run')

    # Todo: check where all of this needs to be - jedi-base-env or one of the bundles?
    depends_on('py-pandas', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-pybind11', type='run')
    depends_on('py-h5py', type='run')
    depends_on('py-netcdf4',  type='run')
    depends_on('py-pycodestyle', type='run')
    depends_on('py-pyyaml', type='run')
    depends_on('py-python-dateutil', type='run')

    depends_on('eccodes', type='run')
    depends_on('py-eccodes', type='run')

    depends_on('bufr', type='run')
