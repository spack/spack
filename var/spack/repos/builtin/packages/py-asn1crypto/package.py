# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyAsn1crypto(PythonPackage):
    """Python ASN.1 library with a focus on performance and a pythonic API """

    homepage = "https://github.com/wbond/asn1crypto"
    url      = "https://pypi.io/packages/source/a/asn1crypto/asn1crypto-0.22.0.tar.gz"

    version('0.22.0', '74a8b9402625b38ef19cf3fa69ef8470')

    depends_on('py-setuptools', type='build')
