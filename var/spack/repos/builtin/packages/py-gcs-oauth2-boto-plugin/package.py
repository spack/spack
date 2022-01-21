# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGcsOauth2BotoPlugin(PythonPackage):
    """Auth plugin allowing use the use of OAuth 2.0 credentials
    for Google Cloud Storage in the Boto library."""

    homepage = "https://github.com/GoogleCloudPlatform/gcs-oauth2-boto-plugin"
    pypi     = "gcs-oauth2-boto-plugin/gcs-oauth2-boto-plugin-2.7.tar.gz"

    maintainers = ['dorton21']

    version('2.7', sha256='c95b011717911a6c40fbd3aa07a8faa0ab57570dee178d7148531327c4c6f93e')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-rsa@:4.0', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-boto@2.29.1:', type=('build', 'run'))
    depends_on('py-google-auth@0.1.0:', type=('build', 'run'))
    depends_on('py-httplib2@0.18:', type=('build', 'run'))
    depends_on('py-oauth2client@2.2.0:', type=('build', 'run'))
    depends_on('py-pyopenssl@0.13:', type=('build', 'run'))
    depends_on('py-retry-decorator@1.0.0:', type=('build', 'run'))
    depends_on('py-six@1.12.0:', type=('build', 'run'))
