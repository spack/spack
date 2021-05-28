# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVisualCortexAnalysis(PythonPackage):
    """Visual cortex analyses"""

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/project/proj120/visual-cortex-analysis'
    git      = 'ssh://bbpcode.epfl.ch/project/proj120/visual-cortex-analysis'

    version('develop', branch='master')

    depends_on('python@3.6:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy',      type=('run'))
    depends_on('py-pandas',     type=('run'))
    depends_on('py-lazy',       type=('run'))
    depends_on('py-tqdm',       type=('run'))
    depends_on('py-pyyaml',     type=('run'))
    depends_on('py-seaborn',    type=('run'))
    depends_on('py-frozendict', type=('run'))
    depends_on('py-bmtk',       type=('run'))
