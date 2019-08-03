# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT

# ----------------------------------------------------------------------------
#
#     spack install py-cachetools
#
# You can edit this file again by typing:
#
#     spack edit py-cachetools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyCachetools(PythonPackage):
    """
    This module provides various memoizing collections and decorators, 
    including variants of the Python 3 Standard Library @lru_cache function decorator. 
    """

    homepage = "https://github.com/tkem/cachetools"
    url      = "https://github.com/tkem/cachetools/archive/v2.1.0.tar.gz"

    version('2.1.0', 'edb7602547104d3a5db96005b16a09d8')

    # Build dependencies
    depends_on('py-setuptools', type='build')

    phases = ['install']



