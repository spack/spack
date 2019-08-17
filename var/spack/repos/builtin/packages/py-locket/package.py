# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLocket(PythonPackage):
    """File-based locks for Python for Linux and Windows."""

    homepage = "http://github.com/mwilliamson/locket.py"
    url      = "https://pypi.io/packages/source/l/locket/locket-0.2.0.tar.gz"

    import_modules = ['locket']

    version('0.2.0', 'fe870949c513d8f7079ba352463833ca')
