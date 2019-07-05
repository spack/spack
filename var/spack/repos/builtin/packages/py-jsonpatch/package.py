# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJsonpatch(PythonPackage):
    """Library to apply JSON Patches according to RFC 6902"""

    homepage = "https://github.com/stefankoegl/python-json-patch"
    url      = "https://github.com/stefankoegl/python-json-patch/archive/v1.23.tar.gz"

    version('1.23', sha256='0af03651204ea3049bc4aedaa42b591e134a4ee16e421f9c5f3ac4e9092885ad')

    depends_on('py-setuptools', type='build')
    depends_on('py-jsonpointer@1.9', type=('build', 'run'))
