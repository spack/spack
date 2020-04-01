# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    url      = "https://pypi.io/packages/source/d/dask/dask-1.1.0.tar.gz"

    version('1.2.2', sha256='5e7876bae2a01b355d1969b73aeafa23310febd8c353163910b73e93dc7e492c')
    version('1.1.2', sha256='93b355b9a9c9a3ddbb39fab99d5759aad5cfd346f4520b87788970e80cf97256')
    version('1.1.0', sha256='e76088e8931b326c05a92d2658e07b94a6852b42c13a7560505a8b2354871454')
    version('0.17.4', sha256='c111475a3d1f8cba41c8094e1fb1831c65015390dcef0308042a11a9606a2f6d')
    version('0.8.1',  sha256='43deb1934cd033668e5e60b735f45c9c3ee2813f87bd51c243f975e55267fa43')

    variant('array',       default=True, description='Install requirements for dask.array')
    variant('bag',         default=True, description='Install requirements for dask.bag')
    variant('dataframe',   default=True, description='Install requirements for dask.dataframe')
    variant('delayed',     default=True, description='Install requirements for dask.delayed')
    variant('distributed', default=True, description='Install requirements for dask.distributed')

    conflicts('+distributed', when='@:1.2.1')  # Only present in 1.2.2+

    depends_on('py-setuptools',         type='build')
    depends_on('py-pytest@3.1.0:',      type='test')
    depends_on('py-requests',           type='test')
    depends_on('py-pytest-runner',      type='test')

    # Requirements for dask.array
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='+array')
    depends_on('py-numpy@1.13.0:',      type=('build', 'run'), when='@1.2.2: +array')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+array')

    # Requirements for dask.bag
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='+bag')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+bag')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='+bag')

    # Requirements for dask.dataframe
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='+dataframe')
    depends_on('py-numpy@1.13.0:',      type=('build', 'run'), when='@1.2.2: +dataframe')
    depends_on('py-pandas@0.19.0:',     type=('build', 'run'), when='+dataframe')
    depends_on('py-pandas@0.21.0:',     type=('build', 'run'), when='@1.2.2: +dataframe')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+dataframe')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='+dataframe')
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='+dataframe')

    # Requirements for dask.delayed
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+delayed')

    # Requirements for dask.distributed
    depends_on('py-distributed@1.22:',  type=('build', 'run'), when='+distributed')

    @property
    def import_modules(self):
        modules = [
            'dask', 'dask.bytes', 'dask.diagnostics', 'dask.store'
        ]

        if '+array' in self.spec:
            modules.append('dask.array')

        if '+bag' in self.spec:
            modules.append('dask.bag')

        if '+dataframe' in self.spec:
            modules.extend([
                'dask.dataframe', 'dask.dataframe.io', 'dask.dataframe.tseries'
            ])

        return modules
