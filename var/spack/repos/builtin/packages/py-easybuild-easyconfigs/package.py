# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildEasyconfigs(PythonPackage):
    """Collection of easyconfig files for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild'
    pypi = 'easybuild-easyconfigs/easybuild-easyconfigs-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.3.2', sha256='efa9d9874d813946c729e217494599492ac4ed02873c9f5a8f793eb9b0bc9e41')
    version('4.3.1', sha256='7892a3c9d2fc4c069941bce751858133fd57ab1f09f0ae69194ac034f8304336')
    version('4.3.0', sha256='48431ddee0d3f36b69dc0dbc2dfca77603a57811ae31f879b9e470a0bf570126')
    version('4.2.2', sha256='de43dcbb5a776c3862f03ab82acb12e1e36c599e517e34017e2c8486106d0db9')
    version('4.2.1', sha256='ace2c4d7d2b020d319a0ab5ee53167c365e3ecb4d437c962d8f486c64395bd71')
    version('4.2.0', sha256='81b57120e0e3ba0d97defafa677a7449fa355b34dfa6ecaca190b5bc94fedffd')
    version('4.1.1', sha256='60dc9527c9c10d15fa040b56f7b44bdf8d2ed6200c323f1f8ab348454e58d91c')
    version('4.1.0', sha256='bfe1f630e2494eca6cbe72d1218f54e10a863c869bce34962d0c79e0b3003716')
    version('4.0.1', sha256='7155d239e586f3fd835089164f46738bd4787f7c5ab0153e33a98976426a7699')
    version('4.0.0', sha256='90d4e8f8abb11e7ae2265745bbd1241cd69d02570e9b4530175c4b2e2aba754e')
    version('3.1.2', sha256='621d514bacd9a0a9a3d35b40dcc448533ffc545b2c79f50d303822778bcc4aa5')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))

    for v in ['@3.1.2', '@4.0.0']:
        depends_on('py-easybuild-framework{0}:'.format(v), when=v + ':', type='run')
        depends_on('py-easybuild-easyblocks{0}:'.format(v), when=v, type='run')
