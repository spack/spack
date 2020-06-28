# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPybtexDocutils(PythonPackage):
    """A docutils backend for pybtex."""

    homepage = "https://pypi.python.org/pypi/pybtex-docutils/"
    url      = "https://pypi.io/packages/source/p/pybtex-docutils/pybtex-docutils-0.2.1.tar.gz"

    import_modules = ['pybtex_docutils']

    version('0.2.1', sha256='e4b075641c1d68a3e98a6d73ad3d029293fcf9e0773512315ef9c8482f251337')

    depends_on('py-setuptools', type='build')
    depends_on('py-docutils@0.8:', type=('build', 'run'))
    depends_on('py-pybtex@0.16:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
