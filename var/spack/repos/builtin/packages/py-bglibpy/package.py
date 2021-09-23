# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBglibpy(PythonPackage):
    """Pythonic Blue Brain simulator access"""
    homepage = "https://bbpgitlab.epfl.ch/cells/bglibpy"
    git = "git@bbpgitlab.epfl.ch:cells/bglibpy.git"

    version('develop', branch='main')

    version('4.4.36', commit='07fe9999a137c3741fd95713149a76a202cb7d7a')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('neuron+python', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-matplotlib@3.0.3:', type='run')
    depends_on('py-cachetools', type='run')
    depends_on('py-h5py@2.3:', type='run')

    depends_on('py-bluepy@2.1:2.999', type='run')
    depends_on('py-libsonata', type='run')

    # skip import test, because bglibpy needs HOC_LIBRARY_PATH
    # that could be provided by neurodamus-core
    import_modules = []

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
