# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyflakes(PythonPackage):
    """A simple program which checks Python source files for errors."""

    homepage = "https://github.com/PyCQA/pyflakes"
    url      = "https://github.com/PyCQA/pyflakes/archive/1.3.0.tar.gz"

    version('1.6.0', '68eff61e54964e6389f8fb1d2122fc5b')
    version('1.5.0', '1dee2ca8a0520061aac5a82f3b539fa0')
    version('1.4.0', 'ed832ef1cbd59463e5f0f6340254f603')
    version('1.3.0', 'a76173deb7a84fe860c0b60e2fbcdfe2')
    version('1.2.3', '2ac2e148a5c46b6bb06c4785be76f7cc')
    version('1.2.2', 'fe759b9381a6500e67a2ddbbeb5161a4')
    version('1.2.1', '444a06b256e0a70e41c11698b7190e84')
    version('1.2.0', '5d1c87bf09696c4c35dc3103f2a1185c')
    version('1.1.0', '4e18bf78c0455ebcd41e5d6104392c88')
    version('1.0.0', 'e2ea22a825c5100f12e54b71771cde71')
    version('0.9.2', 'd02d5f68e944085fd6ec163a34737a96')
    version('0.9.1', '8108d2248e93ca6a315fa2dd31ee9bb1')
    version('0.9.0', '43c2bcee88606bde55dbf25a253ef886')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pyflakes requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
