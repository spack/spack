# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySentryPython(PythonPackage):
    """The new Python SDK for Sentry.io"""

    homepage = "https://github.com/getsentry/sentry-python"
    url = "https://pypi.io/packages/source/s/sentry-sdk/sentry-sdk-0.17.6.tar.gz"

    version('0.17.6', sha256='1a086486ff9da15791f294f6e9915eb3747d161ef64dee2d038a4d0b4a369b24')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.10.0:', type=('build', 'run'))
    depends_on('py-certifi', type=('build', 'run'))
    depends_on('py-flask@0.11:', type=('build', 'run'))
