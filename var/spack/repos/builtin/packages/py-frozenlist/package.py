# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class PyFrozenlist(PythonPackage):
    """A list-like structure which implements collections.abc.MutableSequence."""

    homepage = "https://github.com/aio-libs/frozenlist"
    pypi     = "frozenlist/frozenlist-1.2.0.tar.gz"

    version('1.3.0', sha256='ce6f2ba0edb7b0c1d8976565298ad2deba6f8064d2bebb6ffce2ca896eb35b0b')
    version('1.2.0', sha256='68201be60ac56aff972dc18085800b6ee07973c49103a8aba669dee3d71079de')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
