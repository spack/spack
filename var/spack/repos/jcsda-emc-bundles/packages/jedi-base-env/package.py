# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediBaseEnv(BundlePackage):
    """Basic development environment for JEDI applications"""

    homepage = "https://github.com/noaa-emc/spack-stack"
    git      = "https://github.com/noaa-emc/spack-stack.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')
    version('1.0.0', preferred=True)

    with when('@main'):
        depends_on('base-env',                       type='run')
        depends_on('bison',                          type='run')
        depends_on('blas',                           type='run')
        depends_on('boost',                          type='run')
        depends_on('bufr',                           type='run')
        depends_on('ecbuild',                        type='run')
        depends_on('eccodes',                        type='run')
        depends_on('eckit',                          type='run')
        depends_on('ecmwf-atlas',                    type='run')
        depends_on('eigen',                          type='run')
        depends_on('fckit',                          type='run')
        depends_on('fftw-api',                       type='run')
        depends_on('flex',                           type='run')
        depends_on('git-lfs',                        type='run')
        depends_on('gsl-lite',                       type='run')
        depends_on('hdf',                            type='run')
        depends_on('jedi-cmake',                     type='run')
        depends_on('netcdf-cxx4',                    type='run')
        depends_on('nlohmann-json',                  type='run')
        depends_on('nlohmann-json-schema-validator', type='run')
        depends_on('py-eccodes',                     type='run')
        depends_on('py-h5py',                        type='run')
        depends_on('py-netcdf4',                     type='run')
        depends_on('py-pandas',                      type='run')
        depends_on('py-pycodestyle',                 type='run')
        depends_on('py-pybind11',                    type='run')
        depends_on('py-pyhdf',                       type='run')
        depends_on('py-python-dateutil',             type='run')
        depends_on('py-pyyaml',                      type='run')
        depends_on('py-scipy',                       type='run')
        depends_on('udunits',                        type='run')

    with when('@1.0.0'):
        depends_on('base-env@1.0.0',                 type='run')
        depends_on('bison',                          type='run')
        depends_on('blas',                           type='run')
        depends_on('boost',                          type='run')
        depends_on('bufr',                           type='run')
        depends_on('ecbuild',                        type='run')
        depends_on('eccodes',                        type='run')
        depends_on('eckit@1.19.0',                   type='run')
        depends_on('ecmwf-atlas@0.29.0',             type='run')
        depends_on('eigen@3.4.0',                    type='run')
        depends_on('fckit@0.9.5',                    type='run')
        depends_on('fftw-api',                       type='run')
        depends_on('flex',                           type='run')
        depends_on('git-lfs',                        type='run')
        depends_on('gsl-lite',                       type='run')
        depends_on('hdf@4.2.15',                     type='run')
        depends_on('jedi-cmake@1.3.0',               type='run')
        depends_on('netcdf-cxx4@4.3.1',              type='run')
        depends_on('nlohmann-json',                  type='run')
        depends_on('nlohmann-json-schema-validator', type='run')
        depends_on('py-eccodes',                     type='run')
        depends_on('py-h5py',                        type='run')
        depends_on('py-netcdf4',                     type='run')
        depends_on('py-pandas',                      type='run')
        depends_on('py-pycodestyle',                 type='run')
        depends_on('py-pybind11',                    type='run')
        depends_on('py-pyhdf',                       type='run')
        depends_on('py-python-dateutil',             type='run')
        depends_on('py-pyyaml',                      type='run')
        depends_on('py-scipy',                       type='run')
        depends_on('udunits',                        type='run')


