# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    url      = "https://pypi.io/packages/source/d/dask/dask-1.1.0.tar.gz"

    version('1.1.2', sha256='93b355b9a9c9a3ddbb39fab99d5759aad5cfd346f4520b87788970e80cf97256')
    version('1.1.0', sha256='e76088e8931b326c05a92d2658e07b94a6852b42c13a7560505a8b2354871454')
    version('0.17.4', '4a7b9c5d7ddf52639b1c6b9e8a68d146')
    version('0.8.1',  '5dd8e3a3823b3bc62c9a6d192e2cb5b4')

    variant('array',       default=True, description='Install requirements for dask.array')
    variant('bag',         default=True, description='Install requirements for dask.bag')
    variant('dataframe',   default=True, description='Install requirements for dask.dataframe')
    variant('delayed',     default=True, description='Install requirements for dask.delayed')

    depends_on('py-setuptools',         type='build')
    depends_on('py-pytest@3.1.0:',      type='test')
    depends_on('py-requests',           type='test')

    # Requirements for dask.array
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='+array')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+array')

    # Requirements for dask.bag
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='+bag')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+bag')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='+bag')

    # Requirements for dask.dataframe
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='+dataframe')
    depends_on('py-pandas@0.19.0:',     type=('build', 'run'), when='+dataframe')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+dataframe')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='+dataframe')
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='+dataframe')

    # Requirements for dask.delayed
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='+delayed')

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
