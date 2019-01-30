# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyToolz(PythonPackage):
    """A set of utility functions for iterators, functions, and dictionaries"""

    homepage = "http://github.com/pytoolz/toolz/"
    url      = "https://pypi.io/packages/source/t/toolz/toolz-0.9.0.tar.gz"

    import_modules = ['toolz', 'tlz', 'toolz.curried', 'toolz.sandbox']

    version('0.9.0', '6fd07249389dd0b3bfe71d4282314328')

    depends_on('py-setuptools', type='build')
