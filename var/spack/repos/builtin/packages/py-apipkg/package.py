# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyApipkg(PythonPackage):
    """apipkg: namespace control and lazy-import mechanism"""

    homepage = "https://pypi.python.org/pypi/apipkg"
    url      = "https://pypi.io/packages/source/a/apipkg/apipkg-1.4.tar.gz"

    version('1.4', '17e5668601a2322aff41548cb957e7c8')

    depends_on('py-setuptools', type='build')
