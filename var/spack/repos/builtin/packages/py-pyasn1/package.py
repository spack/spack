# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyPyasn1(PythonPackage):
    """ Generic ASN.1 library for Python http://pyasn1.sf.net"""

    homepage = "https://github.com/etingof/pyasn1"
    url      = "https://pypi.io/packages/source/p/pyasn1/pyasn1-0.2.3.tar.gz"

    version('0.2.3', '79f98135071c8dd5c37b6c923c51be45')
    depends_on('py-setuptools',    type='build')
    depends_on('python@2.4:', type=('build', 'run'))
