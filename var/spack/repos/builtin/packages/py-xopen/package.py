# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXopen(PythonPackage):
    """This small Python module provides a xopen function that works like the
    built-in open function, but can also deal with compressed files. Supported
    compression formats are gzip, bzip2 and xz. They are automatically
    recognized by their file extensions .gz, .bz2 or .xz."""

    homepage = "https://github.com/marcelm/xopen"
    url      = "https://pypi.io/packages/source/x/xopen/xopen-0.1.1.tar.gz"

    version('0.5.0', sha256='b097cd25e8afec42b6e1780c1f6315016171b5b6936100cdf307d121e2cbab9f')
    version('0.1.1', '4e0e955546ee6bee4ea736b54623a671')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:', type=('build', 'run'))
