# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('0.8.2', sha256='003749e09af74103a29e9c64c468c03e084aa6dfe6feff4fe22366679a6534f7')
    version('0.5.0', sha256='b097cd25e8afec42b6e1780c1f6315016171b5b6936100cdf307d121e2cbab9f')
    version('0.1.1', sha256='d1320ca46ed464a59db4c27c7a44caf5e268301e68319f0295d06bf6a9afa6f3')

    depends_on('py-setuptools', type='build')
    depends_on('py-bz2file', type=('build', 'run'), when='@0.5: ^python@:2.8')
    depends_on('python@2.7,3.4:', type=('build', 'run'), when='@0.5:')
    depends_on('python@2.6:2.99,3.3:', type=('build', 'run'), when='@0.1.1')
