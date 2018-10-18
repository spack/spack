# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySingledispatch(PythonPackage):
    """This library brings functools.singledispatch to Python 2.6-3.3."""

    homepage = "https://pypi.python.org/pypi/singledispatch"
    url      = "https://pypi.io/packages/source/s/singledispatch/singledispatch-3.4.0.3.tar.gz"

    version('3.4.0.3', 'af2fc6a3d6cc5a02d0bf54d909785fcb')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))

    # This dependency breaks concretization
    # See https://github.com/spack/spack/issues/2793
    # depends_on('py-ordereddict', when="^python@:2.6", type=('build', 'run'))
