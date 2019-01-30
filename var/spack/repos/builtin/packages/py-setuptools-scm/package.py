# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySetuptoolsScm(PythonPackage):
    """The blessed package to manage your versions by scm tags."""

    homepage = "https://github.com/pypa/setuptools_scm"
    url      = "https://pypi.io/packages/source/s/setuptools_scm/setuptools_scm-3.1.0.tar.gz"

    import_modules = ['setuptools_scm']

    version('3.1.0',  '52a8dee23c9e5f7d7d18094563db516c')
    version('1.15.6', 'f17493d53f0d842bb0152f214775640b')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
