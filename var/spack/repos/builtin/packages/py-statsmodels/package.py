# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStatsmodels(PythonPackage):
    """Statistical computations and models for use with SciPy"""

    homepage = "http://www.statsmodels.org"
    url      = "https://pypi.io/packages/source/s/statsmodels/statsmodels-0.8.0.tar.gz"

    version('0.8.0', 'b3e5911cc9b00b71228d5d39a880bba0')

    variant('plotting', default=False, description='With matplotlib')

    # according to http://www.statsmodels.org/dev/install.html earlier versions
    # might work.
    depends_on('py-setuptools@0.6c5:', type='build')
    depends_on('py-numpy@1.7.0:',      type=('build', 'run'))
    depends_on('py-scipy@0.11:',       type=('build', 'run'))
    depends_on('py-pandas@0.12:',      type=('build', 'run'))
    depends_on('py-patsy@0.2.1:',      type=('build', 'run'))
    depends_on('py-cython@0.24:',      type=('build', 'run'))
    depends_on('py-matplotlib@1.3:',   type='run', when='+plotting')

    # TODO: Add a 'test' deptype
    # depends_on('py-nose', type='test')
