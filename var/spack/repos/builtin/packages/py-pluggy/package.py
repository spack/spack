# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPluggy(PythonPackage):
    """Plugin and hook calling mechanisms for python."""

    homepage = "https://github.com/pytest-dev/pluggy"
    url      = "https://pypi.io/packages/source/p/pluggy/pluggy-0.7.1.tar.gz"

    import_modules = ['pluggy']

    version('0.7.1', 'cd5cc1003143f86dd6e2a865a20f8837')
    version('0.6.0', 'ffdde7c3a5ba9a440404570366ffb6d5')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
