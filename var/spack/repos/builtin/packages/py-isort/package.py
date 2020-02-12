# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    url      = "https://pypi.io/packages/source/i/isort/isort-4.2.15.tar.gz"

    version('4.2.15', sha256='79f46172d3a4e2e53e7016e663cc7a8b538bec525c36675fcfd2767df30b3983')

    depends_on('py-setuptools', type='build')
