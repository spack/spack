# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXarray(PythonPackage):
    """N-D labeled arrays and datasets in Python"""

    homepage = "https://github.com/pydata/xarray"
    url      = "https://pypi.io/packages/source/x/xarray/xarray-0.9.1.tar.gz"

    version('0.9.1', '24cc99f19da95427604846c9d1e20e70')

    depends_on('py-setuptools',      type='build')
    depends_on('py-pandas@0.15.0:',  type=('build', 'run'))
    depends_on('py-numpy@1.7:',      type=('build', 'run'))
