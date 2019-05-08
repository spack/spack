# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxLimestoneTheme(PythonPackage):
    """Sphinx Limestone Theme"""

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BBPSTD/Documentation+Standards"
    git = "ssh://bbpcode.epfl.ch/nse/sphinx-limestone-theme"

    version('0.0.3', tag='sphinx-limestone-theme-v0.0.3', submodules=True, clean=False)

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx@2:', type='run')

    @run_before('build')
    def generate(self):
        python = self.spec['python'].command
        python('translate_templates.py')
