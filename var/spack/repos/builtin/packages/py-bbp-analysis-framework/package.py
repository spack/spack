# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBbpAnalysisFramework(PythonPackage):
    """Bbp analysis framework."""

    homepage = 'https://bbpgitlab.epfl.ch/nse/bbp-analysis-framework'
    git      = 'git@bbpgitlab.epfl.ch:nse/bbp-analysis-framework.git'

    version('1.6.42', commit='5783358e8a8c63055ce5c76d43f55875471cefe8')
    version('1.6.41', commit='75a29902164a855a5ab7921a96aeb1f054284108')
    version('1.6.40', commit='66624837486d8e0783b146b208646eee55bbdb7a')
    version('1.6.39', commit='35eb9e33022bad3f73f377fdeeeabb30245229a6')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-bluepy', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-neurotools', type='run')
    depends_on('py-progressbar', type='run')

    depends_on('py-pdf2image', type='run')
    depends_on('pngquant', type='run')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec['pngquant'].prefix.bin)
