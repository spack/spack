##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyBluepymm(PythonPackage):
    """Blue Brain Model Management Python Library"""

    homepage = "https://github.com/BlueBrain/BluePyMM"
    url = "https://pypi.io/packages/source/b/bluepymm/bluepymm-0.7.15.tar.gz"

    version('0.7.15', sha256='2da2fceed4e3329516f66e522622ab74486ee450b88ecdc107ad0d14d9ff2b21')

    depends_on('py-setuptools', type='build')
    depends_on('py-bluepyopt', type='run')
    depends_on('py-matplotlib', type='run')
    # The below dependency should disappear once
    # the matplotlib package is fixed
    depends_on('py-backports-functools-lru-cache', type='run', when="^python@:3.3.99")
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-ipyparallel', type='run')
    depends_on('py-lxml', type='run')
    depends_on('py-sh', type='run')
    depends_on('neuron', type='run')

    def setup_run_environment(self, env):
        env.unset('PMI_RANK')
        env.set('NEURON_INIT_MPI', "0")
