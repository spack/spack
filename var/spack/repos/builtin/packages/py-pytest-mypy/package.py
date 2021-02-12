# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestMypy(PythonPackage):
    """Mypy static type checker plugin for Pytest."""

    homepage = "https://github.com/dbader/pytest-mypy"
    pypi = "pytest-mypy/pytest-mypy-0.4.2.tar.gz"

    version('0.8.0', sha256='63d418a4fea7d598ac40b659723c00804d16a251d90a5cfbca213eeba5aaf01c')
    version('0.7.0', sha256='5a667d9a2b66bf98b3a494411f221923a6e2c3eafbe771104951aaec8985673d')
    version('0.6.2', sha256='2560a9b27d59bb17810d12ec3402dfc7c8e100e40539a70d2814bcbb27240f27')
    version('0.6.1', sha256='f766b229b2760f99524f2c40c24e3288d4853334e560ab5b59a4ebffb2d4cb1d')
    version('0.6.0', sha256='ea5da19d7343d4ccd98c3fe39cc30dee2743b9fbf00999b2a863e3ead78e353c')
    version('0.5.0', sha256='14c746bd0db5e36618f2fda0ba61ddeb5dc52129ab3923a70f592f934c8887db')
    version('0.4.2', sha256='5a5338cecff17f005b181546a13e282761754b481225df37f33d37f86ac5b304')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest@2.8:',    when='^python@3.5:', type=('build', 'run'))
    depends_on('py-pytest@2.8:4.6', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-mypy@0.500:0.699', when='^python@:3.4',    type=('build', 'run'))
    depends_on('py-mypy@0.500:',      when='^python@3.5:3.7', type=('build', 'run'))
    depends_on('py-mypy@0.700:',      when='^python@3.8:',    type=('build', 'run'))
