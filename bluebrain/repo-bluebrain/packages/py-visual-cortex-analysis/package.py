# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVisualCortexAnalysis(PythonPackage):
    """Visual cortex analyses"""

    homepage = 'https://bbpgitlab.epfl.ch/circuits/proj120/visual-cortex-analysis'
    git      = 'ssh://git@bbpgitlab.epfl.ch/circuits/proj120/visual-cortex-analysis.git'

    version('0.0.0-2022-05-25', commit='e6bffd239a7a5722e7a6f9f5b12bf8d0dc485082')

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy',      type=('run'))
    depends_on('py-pandas',     type=('run'))
    depends_on('py-lazy',       type=('run'))
    depends_on('py-tqdm',       type=('run'))
    depends_on('py-pyyaml',     type=('run'))
    depends_on('py-seaborn',    type=('run'))
    depends_on('py-frozendict', type=('run'))
    depends_on('py-bmtk',       type=('run'))
