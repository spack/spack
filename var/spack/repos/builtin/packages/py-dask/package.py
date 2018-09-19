##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    url      = "https://pypi.io/packages/source/d/dask/dask-0.17.4.tar.gz"

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
