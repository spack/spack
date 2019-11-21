# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStatsmodels(PythonPackage):
    """Statistical computations and models for use with SciPy"""

    homepage = "http://www.statsmodels.org"
    url      = "https://pypi.io/packages/source/s/statsmodels/statsmodels-0.8.0.tar.gz"

    version('0.10.1', sha256='320659a80f916c2edf9dfbe83512d9004bb562b72eedb7d9374562038697fa10')
    version('0.8.0', sha256='26431ab706fbae896db7870a0892743bfbb9f5c83231644692166a31d2d86048')

    variant('plotting', default=False, description='With matplotlib')

    depends_on('python@:3.6', when='@:0.8.0', type=('build', 'run'))

    # according to http://www.statsmodels.org/dev/install.html earlier versions
    # might work.
    depends_on('py-setuptools@0.6c5:', type='build')
    depends_on('py-matplotlib@1.3:',   type=('build', 'run'), when='@0.8.0 +plotting')
    depends_on('py-matplotlib@2.2:',   type=('build', 'run'), when='@0.10.1 +plotting')
    depends_on('py-numpy@1.11.0:',     type=('build', 'run'), when='@0.10.1')
    depends_on('py-numpy@1.7.0:',      type=('build', 'run'), when='@0.8.0')
    depends_on('py-pandas@0.12:',      type=('build', 'run'), when='@0.8.0')
    depends_on('py-pandas@0.19:',      type=('build', 'run'), when='@0.10.1')
    depends_on('py-patsy@0.2.1:',      type=('build', 'run'), when='@0.8.0')
    depends_on('py-patsy@0.4.0:',      type=('build', 'run'), when='@0.10.1')
    depends_on('py-scipy@0.11:',       type=('build', 'run'), when='@0.8.0')
    depends_on('py-scipy@0.18:',       type=('build', 'run'), when='@0.10.1')

    # Tests were not run with the 0.8.0 version of the package.  I've tried
    # enabling them, but they currently fail for v0.10.1 on a mac.
    # see https://github.com/statsmodels/statsmodels/issues/6263
    # depends_on('py-nose', type='test')

