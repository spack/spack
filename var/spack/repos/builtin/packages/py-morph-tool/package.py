# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/morph-tool"
    git      = "ssh://bbpcode.epfl.ch/nse/morph-tool"

    version('develop', branch='master')
    version('0.2.1', tag='morph-tool-v0.2.1')
    version('0.1.14', tag='morph-tool-v0.1.14')

    variant('neuron', default=False, description='Neuron-based functionality')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-bluepyopt', type='run', when='+neuron')
    depends_on('py-click', type='run')
    depends_on('py-functools32', when='^python@:2.99', type='run')
    depends_on('py-morphio', type='run')
    depends_on('py-neurom', type='run', when='@0.1.14:')
    depends_on('py-pathlib2@2.3.5:', type='run')
    depends_on('py-pyyaml', type='run')
