# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJsonpointer(PythonPackage):
    """Library to resolve JSON Pointers according to RFC 6901"""

    homepage = "https://github.com/stefankoegl/python-json-pointer"
    url      = "https://github.com/stefankoegl/python-json-pointer/archive/v2.0.tar.gz"

    version('2.0', sha256='9594b7574a3216c9994181e9db7566a5cafb4ab24956e554f2dba1bb39edecb2')

    depends_on('py-setuptools', type='build')
