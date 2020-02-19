##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyBluepymm(PythonPackage):
    """Blue Brain Model Management Python Library"""

    homepage = "https://github.com/BlueBrain/BluePyMM"
    url = "https://pypi.io/packages/source/b/bluepymm/bluepymm-0.6.35.tar.gz"

    version('0.6.38', sha256='3bba40c3553429b29a1567e5f443a0fae8b477872ea9e400b68d9f19404acc34')

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

    def setup_environment(self, spack_env, run_env):
        run_env.unset('PMI_RANK')
        run_env.set('NEURON_INIT_MPI', "0")
