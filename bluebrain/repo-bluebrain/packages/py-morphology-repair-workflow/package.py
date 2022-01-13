# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMorphologyRepairWorkflow(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://bbpgitlab.epfl.ch/nse/morphology-repair-workflow"
    git      = "git@bbpgitlab.epfl.ch:nse/morphology-repair-workflow.git"

    version('develop', branch='master')
    version('2.0.3', tag='morphology-repair-workflow-v2.0.3')
    version('2.0.2', tag='morphology-repair-workflow-v2.0.2')
    version('1.0.4', tag='morphology-repair-workflow-v1.0.4')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:', type='run')
    depends_on('py-dask+bag', type='run')
    depends_on('py-more-itertools@8.4.0:', type='run')
    depends_on('py-numpy@1.19.1:', type='run')
    depends_on('py-pandas@1.1.0:', type='run')
    depends_on('py-pyyaml@3.10:', type='run')
    depends_on('py-six@1.11.0:', type='run')
    depends_on('py-toolz@0.11.1:', type='run')
    depends_on('py-xmltodict@0.12.0:', type='run')

    depends_on('py-morph-tool@0.2.3:', type='run')
    depends_on('py-morphio@2.5.0:', type='run')
    depends_on('py-neuror@1.1.9:', type='run')
    depends_on('py-neurom@2.0:', type='run')

    depends_on('py-morph-validator@0.2.2:', type='run')
    depends_on('py-neuroc@0.2.4:', type='run')
