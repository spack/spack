# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMechanize(PythonPackage):
    """Stateful programmatic web browsing."""

    homepage = "https://github.com/python-mechanize/mechanize"
    url      = "https://pypi.io/packages/source/m/mechanize/mechanize-0.4.3.tar.gz"

    version('0.4.3', sha256='d7d7068be5e1b3069575c98c870aaa96dd26603fe8c8697b470e2f65259fddbf')

    depends_on('py-setuptools', type='build')
    depends_on('py-html5lib', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
