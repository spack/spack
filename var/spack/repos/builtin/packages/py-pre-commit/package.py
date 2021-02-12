# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit
    hooks."""

    homepage = "https://github.com/pre-commit/pre-commit"
    pypi = "pre_commit/pre_commit-1.20.0.tar.gz"

    version('2.10.1', sha256='399baf78f13f4de82a29b649afd74bef2c4e28eb4f021661fc7f29246e8c7a3a')
    version('2.10.0', sha256='f413348d3a8464b77987e36ef6e02c3372dadb823edf0dfe6fb0c3dc2f378ef9')
    version('2.9.3',  sha256='ee784c11953e6d8badb97d19bc46b997a3a9eded849881ec587accd8608d74a4')
    version('2.9.2',  sha256='e31c04bc23741194a7c0b983fe512801e151a0638c6001c49f2bd034f8a664a1')
    version('2.9.1',  sha256='bf1da4848f2b7f51fd0b5e5bf0131095d7d3c121e8efaaeea5c957e05c365c4e')
    version('2.9.0',  sha256='b2d106d51c6ba6217e859d81774aae33fd825fe7de0dcf0c46e2586333d7a92e')
    version('2.8.2',  sha256='905ebc9b534b991baec87e934431f2d0606ba27f2b90f7f652985f5a5b8b6ae6')
    version('2.8.1',  sha256='8fb2037c404ef8c87125e72564f316cf2bc94fc9c1cb184b8352117de747e164')
    version('2.8.0',  sha256='973b8f53e426266cfb136886a1fcfdbea2ca2641dde77f4ad9b4f9a7e174f742')
    version('2.7.1',  sha256='c54fd3e574565fe128ecc5e7d2f91279772ddb03f8729645fa812fe809084a70')
    version('2.7.0',  sha256='8b1cecd60b7c366c8ca3b37e67c165a1b59cfa913e9b42d390709585ece5af83')
    version('2.6.0',  sha256='1657663fdd63a321a4a739915d7d03baedd555b25054449090f97bb0cb30a915')
    version('2.5.1',  sha256='da463cf8f0e257f9af49047ba514f6b90dbd9b4f92f4c8847a3ccd36834874c7')
    version('2.5.0',  sha256='3f16110d2e5136de8bae11a32e496cc193a68cf02bcf11dba61d8e6aff06efc5')
    version('2.4.0',  sha256='703e2e34cbe0eedb0d319eff9f7b83e2022bb5a3ab5289a6a8841441076514d0')
    version('2.3.0',  sha256='f3e85e68c6d1cbe7828d3471896f1b192cfcf1c4d83bf26e26beeb5941855257')
    version('2.2.0',  sha256='c0aa11bce04a7b46c5544723aedf4e81a4d5f64ad1205a30a9ea12d5e81969e1')
    version('2.1.1',  sha256='f8d555e31e2051892c7f7b3ad9f620bd2c09271d87e9eedb2ad831737d6211eb')
    version('2.1.0',  sha256='5295fb6d652a6c5e0b4636cd2c73183efdf253d45b657ce7367183134e806fe1')
    version('2.0.1',  sha256='bf80d9dd58bea4f45d5d71845456fdcb78c1027eda9ed562db6fa2bd7a680c3a')
    version('2.0.0',  sha256='4acd87f8e4eca44acc1cb8e929058a0e0498a134827ebecba2b1fbe4c799a9a0')
    version('1.21.0', sha256='8f48d8637bdae6fa70cc97db9c1dd5aa7c5c8bf71968932a380628c25978b850')
    version('1.20.0', sha256='9f152687127ec90642a2cc3e4d9e1e6240c4eb153615cb02aa1ad41d331cbb6e')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-aspy-yaml', type=('build', 'run'))
    depends_on('py-cfgv@2.0.0:', type=('build', 'run'))
    depends_on('py-identify@1.0.0:', type=('build', 'run'))
    depends_on('py-nodeenv@0.11.1:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))
    depends_on('py-virtualenv@15.2:', type=('build', 'run'))
    depends_on('py-futures', type=('build', 'run'), when='^python@:3.1.99')
    depends_on('py-importlib-metadata', type=('build', 'run'), when='^python@:3.7.99')
    depends_on('py-importlib-resources', type=('build', 'run'), when='^python@:3.6.99')
