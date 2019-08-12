# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCertifi(PythonPackage):
    """Certifi: A carefully curated collection of Root Certificates for validating
    the trustworthiness of SSL certificates while verifying the identity of TLS
    hosts."""

    homepage = "http://certifi.io/"
    url      = "https://pypi.io/packages/source/c/certifi/certifi-2019.6.16.tar.gz"

    import_modules = ['certifi']

    version('2019.6.16', sha256='945e3ba63a0b9f577b1395204e13c3a231f9bc0223888be653286534e5873695')
    version('2017.4.17', sha256='f7527ebf7461582ce95f7a9e03dd141ce810d40590834f4ec20cddd54234c10a')
    version('2017.1.23',  'b72521a8badff5e89a8eabea586d79ab')
    version('2016.02.28', '5ccfc23bd5e931863f0b01ef3e9d2dbd3bef0e1b')

    depends_on('py-setuptools', type='build')
