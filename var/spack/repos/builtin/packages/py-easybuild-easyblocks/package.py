# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildEasyblocks(PythonPackage):
    """Collection of easyblocks for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild'
    pypi = 'easybuild-easyblocks/easybuild-easyblocks-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.3.2', sha256='128e1fab51895483638cbf3f4c5d96a4d74428483565d0ef5e7dcf6175330eeb')
    version('4.3.1', sha256='b77af0dfe31fe44f01a1b5c64c320d64e3cef4dac9123009df7bb72cd5e06580')
    version('4.3.0', sha256='06598715848db38f6633831d9555b8a1c2aca3023cbe5b33b85778acf8a65174')
    version('4.2.2', sha256='52cd3617862ac878970805a088fad348e9eb9fdec4b789a98feb54a7e3d6463f')
    version('4.2.1', sha256='1a38d4acc663f3b4f39cd4bee443681147dc911102854d0917096707b523deba')
    version('4.2.0', sha256='3619fcd79b8c4f9ff3c913f8d76586c4388f1ec48c90d99140bd230da5631776')
    version('4.1.1', sha256='d82b2dee51f79d4161b65e6aa5cfc26074c09a53408bdbf7cca23a305be01a79')
    version('4.1.0', sha256='f6e017d703334e6008acfb9d28e97aecddef4bf04b24890f3e98b6d5cacc08bd')
    version('4.0.1', sha256='a119a80847e9c51b61005dda074c8b109226318553943348dc36d7607881a980')
    version('4.0.0', sha256='a0fdef6c33c786e323bde1b28bab942fd8e535c26842877d705e692e85b31b07')
    version('3.1.2', sha256='5dcea0d612c5da92815f2c99a591dd2843fe9d76f4c0f4ff4a245d43c39001d8')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))

    for v in ['@3.1.2', '@4.0.0']:
        depends_on('py-easybuild-framework' + v, when=v, type='run')
