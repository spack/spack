# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBglibpy(PythonPackage):
    """Pythonic Blue Brain simulator access"""
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/sim/BGLibPy"
    git      = "ssh://bbpcode.epfl.ch/sim/BGLibPy"

    version('develop', branch='master')
    version('4.0.17', commit='e90513f52a7d9ca3c16877ae7a2bcb8df31c8545', preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('neuron+python', type='run')
    depends_on('py-h5py~mpi@2.3:', type='run')

    depends_on('py-bluepy@0.13.2:', type='run')
