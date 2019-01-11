# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOlefile(PythonPackage):
    """Python package to parse, read and write Microsoft OLE2 files"""

    homepage = "https://www.decalage.info/python/olefileio"
    url      = "https://pypi.io/packages/source/o/olefile/olefile-0.44.zip"

    import_modules = ['olefile']

    version('0.44', 'fc625554e4e7f0c2ddcd00baa3c74ff5')

    depends_on('python@2.6:', type=('build', 'run'))
