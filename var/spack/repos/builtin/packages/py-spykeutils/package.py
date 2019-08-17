# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySpykeutils(PythonPackage):
    """Utilities for analyzing electrophysiological data"""

    homepage = "https://github.com/rproepp/spykeutils"
    url      = "https://pypi.io/packages/source/s/spykeutils/spykeutils-0.4.3.tar.gz"

    version('0.4.3', 'cefe4c48ebfdb9bac7a6cbfaf49dd485')

    depends_on('py-setuptools',       type='build')
    depends_on('py-scipy',            type=('build', 'run'))
    depends_on('py-quantities',       type=('build', 'run'))
    depends_on('py-neo@0.2.1:0.3.99', type=('build', 'run'))
