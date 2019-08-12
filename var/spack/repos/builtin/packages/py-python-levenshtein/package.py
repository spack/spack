# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonLevenshtein(PythonPackage):
    """Python extension for computing string edit distances and
    similarities."""

    homepage = "https://github.com/ztane/python-Levenshtein"
    url      = "https://pypi.io/packages/source/p/python-Levenshtein/python-Levenshtein-0.12.0.tar.gz"

    version('0.12.0', 'e8cde197d6d304bbdc3adae66fec99fb')

    depends_on('py-setuptools', type='build')
