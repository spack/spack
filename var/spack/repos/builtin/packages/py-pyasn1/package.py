# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyPyasn1(PythonPackage):
    """Pure-Python implementation of ASN.1 types and DER/BER/CER codecs
    (X.208)."""

    homepage = "https://github.com/etingof/pyasn1"
    url      = "https://pypi.io/packages/source/p/pyasn1/pyasn1-0.4.6.tar.gz"

    version('0.4.6', sha256='b773d5c9196ffbc3a1e13bdf909d446cad80a039aa3340bcad72f395b76ebc86')
    version('0.2.3', '79f98135071c8dd5c37b6c923c51be45')

    depends_on('python@2.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
