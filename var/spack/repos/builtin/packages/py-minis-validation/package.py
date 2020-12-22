# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMinisValidation(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/minis-validation"
    git      = "ssh://bbpcode.epfl.ch/nse/minis-validation"

    version('develop', branch='master')
    version('0.0.3', tag='minis-validation-v0.0.3')
    version('0.0.2', tag='minis-validation-v0.0.2')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-pandas@0.25:', type='run')
    depends_on('py-matplotlib@3.1.1:', type='run')
    depends_on('py-h5py@2.10:2.99', type='run')
    depends_on('py-click@6.7:', type='run')
    depends_on('py-pyyaml@5.1:', type='run')
    depends_on('py-dask-mpi@2.0:', type='run')
    depends_on('neuron+python@7.8:', type='run')
    depends_on('py-bluepy@0.14:0.99', type='run')
    depends_on('py-neurom@1.4:1.59', type='run')  # temp fix for h5py < 3
    depends_on('py-bluepy-configfile@0.1.10:', type='run')
    depends_on('py-bglibpy@4.3:', type='run')

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
