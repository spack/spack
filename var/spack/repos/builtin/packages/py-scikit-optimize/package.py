# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitOptimize(PythonPackage):
    """Scikit-Optimize, or skopt, is a simple and efficient library to
       minimize (very) expensive and noisy black-box functions. It implements
       several methods for sequential model-based optimization. skopt aims to
       be accessible and easy to use in many contexts.

       The library is built on top of NumPy, SciPy and Scikit-Learn."""

    homepage = "https://scikit-optimize.github.io"
    pypi = "scikit-optimize/scikit-optimize-0.5.2.tar.gz"

    version('0.8.1', sha256='ed5c47818959c91490120b89240527cf5ef36dc3e350dc79e5dbc22edc4ee186')
    version('0.8.0', sha256='1b5aaf09dc68cf4c416a19f639d1ad576cbcba5e78eebae9c40c6320a4d50ce9')
    version('0.7.4', sha256='d193b9505d04dc0aade256f10b08124a5e5679fe8c3e90c09ff9e3a60d9f1752')
    version('0.7.3', sha256='5a77ea64391d79f305b77a84b975ee0915c7f43b5c284fc1b2f03f424114575c')
    version('0.7.2', sha256='211075a1a9c153a355918b9fad4df96ae4dc627a7c16d7b3078912c2e77c0cac')
    version('0.7.1', sha256='850f166caf7cc8d2ab8fde26ffdecf23b3bd8d84a94f7d34994817ef7a898094')
    version('0.7',   sha256='071f7feb050b3dde4dda70c0e6989f5190cf9234fd61363fd2058601f3d8a2f7')
    version('0.5.2', sha256='1d7657a4b8ef9aa6d81e49b369c677c584e83269f11710557741d3b3f8fa0a75')

    variant('plots', default=True,
            description='Build with plot support from py-matplotlib')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy@0.14.0:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.19.1:', type=('build', 'run'))

    depends_on('py-matplotlib',   when='+plots')
