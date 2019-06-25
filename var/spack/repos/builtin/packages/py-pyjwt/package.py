# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyjwt(PythonPackage):
    """JSON Web Token implementation in Python."""

    homepage = "https://pyjwt.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/pyjwt/PyJWT-1.7.1.tar.gz"

    version('1.7.1', 'a4712f980c008696e13e09504120b2a0')

    depends_on('py-setuptools', type='build')
