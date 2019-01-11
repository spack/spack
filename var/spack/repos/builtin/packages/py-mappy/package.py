# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMappy(PythonPackage):
    """Mappy provides a convenient interface to minimap2."""

    homepage = "https://pypi.python.org/pypi/mappy"
    url      = "https://pypi.io/packages/source/m/mappy/mappy-2.2.tar.gz"

    version('2.2', 'dfc2aefe98376124beb81ce7dcefeccb')

    depends_on('zlib')
