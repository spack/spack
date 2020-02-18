# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAstropyHelpers(PythonPackage):
    """The astropy-helpers package includes many build,
    installation, and documentation-related tools used by the
    Astropy project, but packaged separately for use by other
    projects that wish to leverage this work."""

    homepage = "https://github.com/astropy/astropy-helpers"
    url      = "https://github.com/astropy/astropy-helpers/archive/v4.0.1.tar.gz"

    version('4.0.1',  sha256='88602971c3b63d6aaa6074d013f995d1e234acb3d517d70d7fcebd30cdaf5c89')
    version('4.0rc1', sha256='322aeda0ff0c8459efc6306b4d26eb115d09e96946f48f1dfe6e91f41ea6af1a')
    version('4.0',    sha256='ca50fdcbe432fb101bbedda6db3cd256ab8b52a9b402ac4fc1c488cc79d11dba')
    version('3.2.2',  sha256='101b657b6d5785ab26c11082125340655578698ca6c38c2ddb33d73c1084a8f4')
    version('3.2.1',  sha256='2638157c65bbf92530b7ecc86bc62c16ec4bc5ccc533f0d96d014f605a8386a3')
    version('3.2rc1', sha256='f9a5ae63a46f78af032a656c14790ff3ed63773c574adf0fb7ddf3a916d54ddb')
    version('3.2',    sha256='0671f70eb67f82d32c23d6b30542c7a1985335ed2fb5e95eb1804bf333258c5b')
    version('3.1.1',  sha256='8ba7e693f1cc9a1c12be3b4ba9e65b67246bff1741c726b79a6dc7b233ba4cd4')
    version('2.0.11', sha256='0cfca63fe2d9920ac1138ffd0a977572b41439e02f6f500f6f62981ef138f0ca')
    version('2.0.10', sha256='528421568531719447677df73f547c25305fbd116c6692faa0f268eac4a3e6d6')

    depends_on('py-setuptools@30.3:', type='build')
    depends_on('py-astropy')

    def build_args(self, spec, prefix):
        args = []
        return args
