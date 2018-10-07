# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    url      = "https://pypi.io/packages/source/i/isort/isort-4.2.15.tar.gz"

    version('4.2.15', '34915a2ce60e6fe3dbcbf5982deef9b4')

    depends_on('py-setuptools', type='build')
