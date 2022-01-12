# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHttplib2(PythonPackage):
    """A comprehensive HTTP client library."""

    homepage = "https://github.com/httplib2/httplib2"
    pypi = "httplib2/httplib2-0.13.1.tar.gz"

    version('0.18.0', sha256='b0e1f3ed76c97380fe2485bc47f25235453b40ef33ca5921bb2897e257a49c4c')
    version('0.13.1', sha256='6901c8c0ffcf721f9ce270ad86da37bc2b4d32b8802d4a9cec38274898a64044')

    depends_on('py-setuptools', type='build')
