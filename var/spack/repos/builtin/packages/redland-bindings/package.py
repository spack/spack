# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RedlandBindings(AutotoolsPackage):
    """Redland Language Bindings for language APIs to Redland"""

    homepage = "http://librdf.org/"
    url      = "http://download.librdf.org/source/redland-bindings-1.0.17.1.tar.gz"

    version('1.0.17.1', sha256='ff72b587ab55f09daf81799cb3f9d263708fad5df7a5458f0c28566a2563b7f5')
    version('1.0.16.1', sha256='065037ef61e9b78f642e75b9c2a42700eb1a87d903f2f9963d86591c7d916826')
    version('1.0.14.1', sha256='a8cc365fccf292c56d53341ecae57fe8727e5002e048ca25f6251b5e595aec40')

    depends_on('swig')
    depends_on('redland')
    depends_on('python')
    depends_on('krb5')
    depends_on('libssh')
    extends('python')

    def configure_args(self):
        args = []
        args.append('--with-python')
        python_version = self.spec['python'].version.up_to(2)
        plib = join_path(
            self.prefix.lib,
            'python{0}'.format(python_version),
            'site-packages'
        )
        args.append('PYTHON_LIB={0}'.format(plib))
        return args
