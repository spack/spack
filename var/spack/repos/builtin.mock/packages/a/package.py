# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class A(AutotoolsPackage):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')
    version('2.0', '2.0_a_hash')

    variant(
        'foo',
        values=('bar', 'baz', 'fee'),
        default='bar',
        description='',
        multi=True
    )

    variant(
        'foobar',
        values=('bar', 'baz', 'fee'),
        default='bar',
        description='',
        multi=False
    )

    variant('bvv', default=True, description='The good old BV variant')

    depends_on('b', when='foobar=bar')

    def with_or_without_fee(self, activated):
        if not activated:
            return '--no-fee'
        return '--fee-all-the-time'

    def autoreconf(self, spec, prefix):
        pass

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        pass
