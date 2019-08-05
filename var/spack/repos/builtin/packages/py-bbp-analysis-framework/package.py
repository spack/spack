# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBbpAnalysisFramework(PythonPackage):
    """Bbp analysis framework."""

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/nse/bbp-analysis-framework'
    git      = 'ssh://bbpcode.epfl.ch/nse/bbp-analysis-framework'

    version('0.6.39', commit='31ae2d32c002c1601837577bfcfab71d41feb89e')

    depends_on('python@:2', type=('build', 'run'))

    depends_on('py-setuptools', type=('build'))

    depends_on('py-bluepy', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-neurotools', type='run')
