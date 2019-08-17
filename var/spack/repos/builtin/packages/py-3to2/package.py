# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Py3to2(PythonPackage):
    """lib3to2 is a set of fixers that are intended to backport code written
    for Python version 3.x into Python version 2.x."""

    homepage = "https://pypi.python.org/pypi/3to2"
    url      = "https://pypi.io/packages/source/3/3to2/3to2-1.1.1.zip"

    version('1.1.1', 'cbeed28e350dbdaef86111ace3052824')
