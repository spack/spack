##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetpyne(PythonPackage):
    """Netpyne: A python package to facilitate the development,
     parallel simulation, optimization and analysis of multiscale
    biological neuronal networks in NEURON."""

    homepage = "http://www.netpyne.org/"
    git      = "https://github.com/Neurosim-lab/netpyne.git"

    version('develop', git=git, branch='master')
    version('0.9.6', git=git, tag='v0.9.6')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-future', type='run')
    depends_on('py-matplotlib@2.2:', type='run')
    depends_on('py-matplotlibscalebar', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-scipy', type='run')

    depends_on('python@3.6:')
    depends_on('neuron+coreneuron+python', type='run')
