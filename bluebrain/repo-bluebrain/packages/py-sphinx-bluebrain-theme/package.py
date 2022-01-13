# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxBluebrainTheme(PythonPackage):
    """Sphinx BlueBrain Theme is the standard Blue Brain Project
    documentation theme."""

    homepage = "https://github.com/BlueBrain/sphinx-bluebrain-theme.git"
    url = "https://pypi.io/packages/source/s/sphinx-bluebrain-theme/sphinx-bluebrain-theme-0.2.4.tar.gz"

    version('0.2.4', sha256='4b3978dd3fe4aa3164ccb72e64117c4211432868e19cc9950fefdaa1d3b9bc1e')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-sphinx@2.0.0:', type=('build', 'run'))
