# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEcdsa(PythonPackage):
    """Pure-Python Elliptic Curve Digital Signature Algorithm signature/verification."""

    homepage = "https://github.com/warner/python-ecdsa"
    url      = "https://pypi.io/packages/source/e/ecdsa/ecdsa-0.13.2.tar.gz"

    version('0.13.2', '0ce51d17c0751e5232be4eafd69b7f13')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-six', type='run')
