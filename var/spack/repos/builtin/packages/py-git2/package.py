# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "http://www.pygit2.org/"
    url      = "https://pypi.io/packages/source/p/pygit2/pygit2-0.24.1.tar.gz"

    version('0.24.1', 'dd98b6a9fded731e36ca5a40484c8545')

    extends('python')
    depends_on('py-setuptools', type='build')
    # Version must match with libgit2
    # See: http://www.pygit2.org/install.html
    depends_on('libgit2@0.24:', when='@0.24:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        # http://www.pygit2.org/install.html
        spack_env.set('LIBGIT2', spec['libgit2'].prefix)
        spack_env.set('LIBGIT2_LIB', spec['libgit2'].prefix.lib)
