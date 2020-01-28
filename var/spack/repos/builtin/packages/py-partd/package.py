# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPartd(PythonPackage):
    """Key-value byte store with appendable values."""

    homepage = "http://github.com/dask/partd/"
    url      = "https://pypi.io/packages/source/p/partd/partd-0.3.8.tar.gz"

    import_modules = ['partd']

    version('0.3.8', sha256='67291f1c4827cde3e0148b3be5d69af64b6d6169feb9ba88f0a6cfe77089400f')

    depends_on('py-setuptools', type='build')
    depends_on('py-locket', type=('build', 'run'))
    depends_on('py-toolz', type=('build', 'run'))
