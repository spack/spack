# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyGoogleapisCommonProtos(PythonPackage):
    """Common protobufs used in Google APIs."""

    homepage = "https://github.com/googleapis/googleapis"
    pypi = "googleapis-common-protos/googleapis-common-protos-1.6.0.tar.gz"

    version('1.55.0', sha256='53eb313064738f45d5ac634155ae208e121c963659627b90dfcb61ef514c03e1')
    version('1.6.0', sha256='e61b8ed5e36b976b487c6e7b15f31bb10c7a0ca7bd5c0e837f4afab64b53a0c6')

    depends_on('py-setuptools', type='build')
    depends_on('py-protobuf@3.6.0:3', type=('build', 'run'))
    depends_on('py-protobuf@3.12.0:3', type=('build', 'run'), when='@1.55.0:')
