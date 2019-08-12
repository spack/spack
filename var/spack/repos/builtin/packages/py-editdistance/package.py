# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEditdistance(PythonPackage):
    """Fast implementation of the edit distance (Levenshtein distance)."""

    homepage = "https://github.com/aflc/editdistance"
    url      = "https://pypi.io/packages/source/e/editdistance/editdistance-0.4.tar.gz"

    version('0.4', '27434720ca0930a9b6974b182b6237bc')

    depends_on('py-setuptools', type='build')
