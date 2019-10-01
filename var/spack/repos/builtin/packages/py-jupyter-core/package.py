# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterCore(PythonPackage):
    """Core Jupyter functionality"""

    homepage = "http://jupyter-core.readthedocs.io/"
    url      = "https://github.com/jupyter/jupyter_core/archive/4.2.0.tar.gz"

    version('4.4.0', 'f2bdb8be2959d3043b77508dd6498687')
    version('4.2.0', '25c1fc68b1b73c0a2e616c76f02bf061')
    version('4.1.1', '2fce5ff60291bc01b39b1f00b3cbb784')
    version('4.1.0', 'b7e928f965f68aef13fea1bf9d6384aa')
    version('4.0.6', '50a73c3a4a8ed047a3674d2b5274cc3b')
    version('4.0.5', 'c09bd3be58f141b49b90cdb2ba22f77f')
    version('4.0.4', '5b6ca0e73bf559f4fe6106a6e412f913')
    version('4.0.3', 'f2608f6e92f992ec8e37646b52c922a6')
    version('4.0.2', 'ae0d0197c4febf43c050a97ac6277263')
    version('4.0.1', 'f849136b2badaaba2a8a3b397bf04639')
    version('4.0',   'b6b37cb4f40bd0fcd20433cb2cc7a4c1')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-traitlets', type=('build', 'run'))
