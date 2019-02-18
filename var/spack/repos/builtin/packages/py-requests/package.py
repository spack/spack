# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRequests(PythonPackage):
    """Python HTTP for Humans."""

    homepage = "http://python-requests.org"
    url = "https://pypi.io/packages/source/r/requests/requests-2.14.2.tar.gz"

    import_modules = [
        'requests', 'requests.packages', 'requests.packages.chardet',
        'requests.packages.urllib3', 'requests.packages.idna',
        'requests.packages.chardet.cli', 'requests.packages.urllib3.util',
        'requests.packages.urllib3.packages',
        'requests.packages.urllib3.contrib',
        'requests.packages.urllib3.packages.ssl_match_hostname',
        'requests.packages.urllib3.packages.backports',
        'requests.packages.urllib3.contrib._securetransport'
    ]

    version('2.14.2', '4c3c169ed67466088a2a6947784fe444')
    version('2.13.0', '921ec6b48f2ddafc8bb6160957baf444')
    version('2.11.1', 'ad5f9c47b5c5dfdb28363ad7546b0763')
    version('2.3.0',  '7449ffdc8ec9ac37bbcd286003c80f00')

    depends_on('py-setuptools', type='build')

    depends_on('py-pytest@2.8.0:',        type='test')
    depends_on('py-pytest-cov',           type='test')
    depends_on('py-pytest-httpbin@0.0.7', type='test')
    depends_on('py-pytest-mock',          type='test')
