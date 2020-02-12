# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mozjs(AutotoolsPackage):
    """SpiderMonkey is Mozilla's JavaScript engine written in C/C++.
    It is used in various Mozilla products, including Firefox, and is
    available under the MPL2."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey"

    version('24.2.0', sha256='e62f3f331ddd90df1e238c09d61a505c516fe9fd8c5c95336611d191d18437d8',
            url="http://ftp.mozilla.org/pub/js/mozjs-24.2.0.tar.bz2")
    version('17.0.0', sha256='321e964fe9386785d3bf80870640f2fa1c683e32fe988eeb201b04471c172fba',
            url="http://ftp.mozilla.org/pub/js/mozjs17.0.0.tar.gz")
    version('1.8.5',  sha256='5d12f7e1f5b4a99436685d97b9b7b75f094d33580227aa998c406bbae6f2a687',
            url="http://ftp.mozilla.org/pub/js/js185-1.0.0.tar.gz")

    depends_on('perl@5.6:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7.3:2.8', type='build')
    depends_on('nspr', when='@:27')
    depends_on('libffi@3.0.9:')
    depends_on('readline')
    depends_on('zlib@1.2.3')

    configure_directory = 'js/src'
    build_directory = 'js/src/spack-build'

    patch('perl-bug.patch')

    def configure_args(self):
        spec = self.spec
        return [
            '--enable-readline',    # enables readline support in JS shell
            '--enable-threadsafe',  # enables support for multiple threads
            '--enable-system-ffi',
            '--with-system-zlib={0}'.format(spec['zlib'].prefix),
            '--with-system-nspr',
            '--with-nspr-prefix={0}'.format(spec['nspr'].prefix),
        ]
