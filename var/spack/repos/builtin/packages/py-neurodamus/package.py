# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyNeurodamus(PythonPackage):
    """The BBP simulation control suite, Python API
    """

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BGLIB/Neurodamus"
    git      = "ssh://bbpcode.epfl.ch/sim/neurodamus-py"

    version('develop', branch='master')
    version('0.7.1',   tag='0.7.1')

    # We depend on Neurodamus but let the user decide which one
    depends_on('python@3.4:',      type=('build', 'run'))
    depends_on('py-setuptools',    type=('build', 'run'))
    depends_on('py-h5py',          type='run')
    depends_on('py-numpy',         type='run')
    depends_on('py-lazy-property', type='run')
    depends_on('py-docopt',        type='run')
