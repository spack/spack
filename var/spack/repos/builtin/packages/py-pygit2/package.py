# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "https://www.pygit2.org/"
    pypi = "pygit2/pygit2-0.24.1.tar.gz"

    version('1.6.0', sha256='7aacea4e57011777f4774421228e5d0ddb9a6ddb87ac4b542346d17ab12a4d62')
    version('1.4.0', sha256='cbeb38ab1df9b5d8896548a11e63aae8a064763ab5f1eabe4475e6b8a78ee1c8')
    version('1.3.0', sha256='0be93f6a8d7cbf0cc79ae2f0afb1993fc055fc0018c27e2bd01ba143e51d4452')
    version('0.28.2', sha256='4d8c3fbbf2e5793a9984681a94e6ac2f1bc91a92cbac762dbdfbea296b917f86')
    version('0.24.1', sha256='4d1d0196b38d6012faf0a7c45e235c208315672b6035da504566c605ba494064')

    depends_on('py-setuptools', type='build')
    # Version must match with libgit2
    # See: https://www.pygit2.org/install.html
    depends_on('libgit2@1.1.0:1.1', when='@1.4:')
    depends_on('libgit2@1.0.0:1.0', when='@1.2:1.3')
    depends_on('libgit2@0:1.0', when='@1.1.0:1.1')
    depends_on('libgit2@0.28.0:0.28', when='@0.28:1.0')
    depends_on('libgit2@0.24:0.27', when='@0.24:0.27')
    depends_on('python@3.6:', when='@1.4.0:')
    depends_on('python@3.6:3.8', when='@1.2:1.3')
    depends_on('python@3.5:3.8', when='@1.0:1.1')
    depends_on('python@2.7:3.7', when='@0.28:0')
    depends_on('py-six', type=('build', 'run'), when='@:0.28.2')
    depends_on('py-cffi@1.4.0:', type=('build', 'run'))
    depends_on('py-cached-property', when='@1.1.0:1.5', type=('build', 'run'))
    depends_on('py-cached-property', when='@1.6.0: ^python@:3.7', type=('build', 'run'))

    def setup_build_environment(self, env):
        spec = self.spec
        # https://www.pygit2.org/install.html
        env.set('LIBGIT2', spec['libgit2'].prefix)
        env.set('LIBGIT2_LIB', spec['libgit2'].prefix.lib)
