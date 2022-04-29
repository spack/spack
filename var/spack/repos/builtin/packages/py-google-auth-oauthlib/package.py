# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class PyGoogleAuthOauthlib(PythonPackage):
    """This library provides oauthlib integration with google-auth."""

    homepage = "https://github.com/googleapis/google-auth-library-python-oauthlib"
    pypi = "google-auth-oauthlib/google-auth-oauthlib-0.4.1.tar.gz"

    version('0.4.6', sha256='a90a072f6993f2c327067bf65270046384cda5a8ecb20b94ea9a687f1f233a7a')
    version('0.4.1', sha256='88d2cd115e3391eb85e1243ac6902e76e77c5fe438b7276b297fbe68015458dd')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@0.4.6:')
    depends_on('py-setuptools', type='build')
    depends_on('py-google-auth', type=('build', 'run'))
    depends_on('py-google-auth@1.0.0:', type=('build', 'run'), when='@0.4.6:')
    depends_on('py-requests-oauthlib@0.7.0:', type=('build', 'run'))
