# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMypy(PythonPackage):
    """Optional static typing for Python."""

    homepage = "http://www.mypy-lang.org/"
    pypi = "mypy/mypy-0.740.tar.gz"

    version('0.920', sha256='a55438627f5f546192f13255a994d6d1cf2659df48adcf966132b4379fd9c86b')
    version('0.910', sha256='704098302473cb31a218f1775a873b376b30b4c18229421e9e9dc8916fd16150')
    version('0.900', sha256='65c78570329c54fb40f956f7645e2359af5da9d8c54baa44f461cdc7f4984108')
    version('0.800', sha256='e0202e37756ed09daf4b0ba64ad2c245d357659e014c3f51d8cd0681ba66940a')
    version('0.790', sha256='2b21ba45ad9ef2e2eb88ce4aeadd0112d0f5026418324176fd494a6824b74975')
    version('0.740', sha256='48c8bc99380575deb39f5d3400ebb6a8a1cb5cc669bbba4d3bb30f904e0a0e7d')

    variant('python2', default=False, description='Enable checking of python 2 type annotations')

    depends_on('python@3.6:', when='@0.920:', type=('build', 'run'))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on('py-setuptools@40.6.2:', when='@0.790:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-wheel@0.30:', when='@0.790:', type='build')
    depends_on('py-typed-ast@1.4.0:1', when='@0.920: ^python@:3.7', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.0:1.4', when='@0.900:0.910 ^python@:3.7', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.0:1.4', when='@:0.800', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4:', type=('build', 'run'))
    depends_on('py-mypy-extensions@0.4.3:0.4', type=('build', 'run'))
    depends_on('py-tomli@1.1:2', when='@0.920:', type=('build', 'run'))
    depends_on('py-toml', when='@0.900:0.910', type=('build', 'run'))
