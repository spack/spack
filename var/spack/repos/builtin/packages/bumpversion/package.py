# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bumpversion(PythonPackage):
    """Version-bump your software with a single command."""

    homepage = "https://pypi.python.org/pypi/bumpversion"
    url      = "https://pypi.io/packages/source/b/bumpversion/bumpversion-0.5.0.tar.gz"

    version('0.5.3', 'c66a3492eafcf5ad4b024be9fca29820')
    version('0.5.0', '222ba619283d6408ce1bfbb0b5b542f3')

    depends_on('py-setuptools', type='build')
