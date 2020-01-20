# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyyaml(PythonPackage):
    """PyYAML is a YAML parser and emitter for Python."""

    homepage = "http://pyyaml.org/wiki/PyYAML"
    url      = "https://pypi.io/packages/source/P/PyYAML/PyYAML-5.1.2.tar.gz"

    version('5.1.2', sha256='01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4')
    version('5.1',   sha256='436bc774ecf7c103814098159fbb84c2715d25980175292c648f2da143909f95')
    version('3.13',  sha256='3ef3092145e9b70e3ddd2c7ad59bdd0252a94dfe3949721633e41344de00a6bf')
    version('3.12',  sha256='592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab')
    version('3.11',  sha256='c36c938a872e5ff494938b33b14aaa156cb439ec67548fcab3535bb78b0846e8')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('libyaml')
