# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyPyrsistent(PythonPackage):
    """Pyrsistent is a number of persistent collections
       (by some referred to as functional data structures).
       Persistent in the sense that they are immutable."""

    homepage = "https://github.com/tobgu/pyrsistent/"
    pypi = "pyrsistent/pyrsistent-0.15.7.tar.gz"

    version('0.18.0', sha256='773c781216f8c2900b42a7b638d5b517bb134ae1acbebe4d1e8f1f41ea60eb4b')
    version('0.15.7', sha256='cdc7b5e3ed77bed61270a47d35434a30617b9becdf2478af76ad2c6ade307280')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'link', 'run'))
    depends_on('python@3.6:', type=('build', 'link', 'run'), when='@0.18.0:')
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools@42:', type='build', when='@0.18.0:')
    depends_on('py-six', type=('build', 'run'), when='@:0.17')
