# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMinisValidation(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://bbpgitlab.epfl.ch/nse/minis-validation/"
    git      = "git@bbpgitlab.epfl.ch:nse/minis-validation.git"

    version('develop', branch='master')
    version('0.0.5', tag='minis-validation-v0.0.5')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.14:1.999', type='run')
    depends_on('py-pandas@0.25:1.999', type='run')
    depends_on('py-matplotlib@3.1.1:', type='run')
    depends_on('py-h5py@3.0:3.999', type='run')
    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-pyyaml@5.1:5.999', type='run')
    depends_on('py-dask+distributed+bag', type='run')
    depends_on('py-dask-mpi', type='run')
    depends_on('py-distributed', type='run')
    depends_on('neuron+python@7.8:', type='run')
    depends_on('py-bluepy@2.0:2.999', type='run')
    depends_on('py-bluepy-configfile@0.1.10:0.999', type='run')
    depends_on('py-bglibpy@4.4:4.999', type='run')

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
