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
    version('0.10.0', sha256='65f321640e21134fc18b312fb2f3edcfbd23ddc36831a06e2445f9f2d7c01aba')
    version('0.9.0', sha256='6461f93a842c649922c2c9a9bc9d9c4834110b89de8c4af196a791ab8f42ba3b')
    version('0.8.0', sha256='26431ab706fbae896db7870a0892743bfbb9f5c83231644692166a31d2d86048')

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

    conflicts('^python@3.7:', when='@:0.8.0')
