# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRtree(PythonPackage):
    """R-Tree spatial index for Python GIS."""

    homepage = "https://github.com/Toblerity/rtree"
    pypi = "Rtree/Rtree-0.8.3.tar.gz"

    maintainers = ['adamjstewart']

    version('1.0.0', sha256='d0483482121346b093b9a42518d40f921adf445915b7aea307eb26768c839682')
    version('0.9.7', sha256='be8772ca34699a9ad3fb4cfe2cfb6629854e453c10b3328039301bbfc128ca3e')
    version('0.8.3', sha256='6cb9cf3000963ea6a3db777a597baee2bc55c4fc891e4f1967f262cc96148649')

    depends_on('python@3.7:', when='@1:', type=('build', 'run'))
    depends_on('python@3:', when='@0.9.4:', type=('build', 'run'))
    depends_on('py-setuptools@39.2:', when='@1:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-typing-extensions@3.7:', when='@1: ^python@:3.7', type=('build', 'run'))
    depends_on('libspatialindex@1.8.5:')

    def setup_build_environment(self, env):
        env.set('SPATIALINDEX_C_LIBRARY', self.spec['libspatialindex'].libs[0])

    def setup_run_environment(self, env):
        self.setup_build_environment(env)
