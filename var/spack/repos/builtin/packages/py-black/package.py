# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBlack(PythonPackage):
    """Black is the uncompromising Python code formatter. By using it, you agree to
    cede control over minutiae of hand-formatting. In return, Black gives you
    speed, determinism, and freedom from pycodestyle nagging about formatting.
    """

    homepage = "https://github.com/psf/black"
    pypi = "black/black-20.8b1.tar.gz"

    version('21.7b0', sha256='c8373c6491de9362e39271630b65b964607bc5c79c83783547d76c839b3aa219')
    version('21.6b0', sha256='dc132348a88d103016726fe360cb9ede02cecf99b76e3660ce6c596be132ce04')
    version('21.4b0', sha256='915d916c48646dbe8040d5265cff7111421a60a3dfe7f7e07273176a57c24a34')
    version('20.8b1', sha256='1c02557aa099101b9d21496f8a914e9ed2222ef70336404eeeac8edba836fbea')
    version('19.3b0', sha256='68950ffd4d9169716bcb8719a56c07a2f4485354fec061cdd5910aa07369731c')
    version('18.9b0', sha256='e030a9a28f542debc08acceb273f228ac422798e5215ba2a791a6ddeaaca22a5')

    variant('colorama', default=False, description='enable colorama support')
    variant('d', default=False, description='enable blackd HTTP server')
    variant('python2', default=False, description='enable python 2 formatting support')

    depends_on('python@3.6.0:', type=('build', 'run'))
    depends_on('python@3.6.2:', when='@21:', type=('build', 'run'))
    # Needs setuptools at runtime so that `import pkg_resources` succeeds
    # See #8843 and #8689 for examples of setuptools added as a runtime dep
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', when='@19.10:', type='build')
    # Translated from black's setup.py:
    # https://github.com/ambv/black/blob/master/setup.py
    depends_on('py-click@6.5:', type=('build', 'run'))
    depends_on('py-click@7.1.2:', when='@20.8b1:', type=('build', 'run'))
    depends_on('py-attrs@18.1.0:', when='@:20.8b0', type=('build', 'run'))
    depends_on('py-appdirs', type=('build', 'run'))
    depends_on('py-toml@0.9.4:', when='@:19', type=('build', 'run'))
    depends_on('py-toml@0.10.1:', when='@20:21.6', type=('build', 'run'))
    depends_on('py-tomli@0.2.6:1.999', when='@21.7:', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.0:', when='@19.10b0:20', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.2:', when='@21: ^python@:3.7.999', type=('build', 'run'))
    depends_on('py-regex@2020.1.8:', when='@20.8b0:', type=('build', 'run'))
    depends_on('py-pathspec@0.6:0.999', when='@19.10b0:', type=('build', 'run'))
    depends_on('py-pathspec@0.8.1:0.999', when='@21.6:', type=('build', 'run'))
    depends_on('py-dataclasses@0.6:', when='@20.8b0:^python@:3.6', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4:', when='@20.8b0:20.999', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4:', when='@21: ^python@:3.7.999', type=('build', 'run'))
    depends_on('py-mypy-extensions@0.4.3:', when='@20.8b0:', type=('build', 'run'))
    depends_on('py-colorama@0.4.3:', when='+colorama', type=('build', 'run'))
    depends_on('py-aiohttp@3.3.2:', when='+d', type=('build', 'run'))
    depends_on('py-aiohttp@3.6.0:', when='@21.6: +d', type=('build', 'run'))
    depends_on('py-aiohttp-cors', when='+d', type=('build', 'run'))
    depends_on('py-aiohttp-cors@0.4.0:', when='@21.6: +d', type=('build', 'run'))
    depends_on('py-typed-ast@1.4.2:', when='+python2', type=('build', 'run'))

    @property
    def import_modules(self):
        modules = ['blib2to3', 'blib2to3.pgen2', 'black']

        if '+d' in self.spec:
            modules.append('blackd')

        return modules
