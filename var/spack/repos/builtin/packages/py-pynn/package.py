# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPynn(PythonPackage):
    """A Python package for simulator-independent specification of neuronal
        network models
    """

    homepage = "http://neuralensemble.org/PyNN/"
    url      = "https://pypi.io/packages/source/P/PyNN/PyNN-0.8.3.tar.gz"
    git      = "https://github.com/NeuralEnsemble/PyNN.git"

    version('0.9.1', '3b8a6c63dc59d7ac751029f84dcaf7e6')
    version('0.8.3', '28c63f898093806a57198e9271ed7b82')
    version('0.8beta', commit='ffb0cb1661f2b0f2778db8f71865978fe7a7a6a4')
    version('0.8.1', '7fb165ed5af35a115cb9c60991645ae6')
    version('0.7.5', 'd8280544e4c9b34b40fd372b16342841')

    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-jinja2@2.7:',        type=('build', 'run'))
    depends_on('py-docutils@0.10:',     type=('build', 'run'))
    depends_on('py-numpy@1.5:',         type=('build', 'run'))
    depends_on('py-quantities@0.10:',   type=('build', 'run'))
    depends_on('py-lazyarray@0.2.9:',   type=('build', 'run'))

    depends_on('py-neo@0.3:0.4.1',      type=('build', 'run'), when="@:0.8.3")
    depends_on('py-neo@0.5.0:',         type=('build', 'run'), when="@0.9.0:")

    depends_on('py-mock@1.0:', type='test')
