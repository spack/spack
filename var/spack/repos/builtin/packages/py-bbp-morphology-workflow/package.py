# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyBbpMorphologyWorkflow(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/platform/bbp-morphology-workflow"
    git      = "ssh://bbpcode.epfl.ch/platform/bbp-morphology-workflow"
    version('develop', branch='master')
    version('1.0.1', tag='morphology-repair-workflow-v1.0.1')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-neuroc', type='run')
    depends_on('py-morph-tool', type='run')
    depends_on('py-morph-repair', type='run')
