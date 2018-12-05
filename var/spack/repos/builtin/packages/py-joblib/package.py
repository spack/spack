# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJoblib(PythonPackage):
    """Python function as pipeline jobs"""

    homepage = "http://packages.python.org/joblib/"
    url      = "https://pypi.io/packages/source/j/joblib/joblib-0.10.3.tar.gz"

    version('0.10.3', '455401ccfaf399538d8e5333086df2d3')
    version('0.10.2', 'ebb42af4342c2445b175f86bd478d869')
    version('0.10.0', '61e40322c4fed5c22905f67d7d1aa557')

    # for testing
    # depends_on('py-nose', type=('build', 'run'))
