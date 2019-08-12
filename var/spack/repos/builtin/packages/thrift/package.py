# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Thrift(Package):
    """Software framework for scalable cross-language services development.

    Thrift combines a software stack with a code generation engine to
    build services that work efficiently and seamlessly between C++,
    Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa,
    JavaScript, Node.js, Smalltalk, OCaml and Delphi and other languages.

    """

    homepage = "http://thrift.apache.org"
    url      = "http://apache.mirrors.ionfish.org/thrift/0.9.2/thrift-0.9.2.tar.gz"

    version('0.11.0', '0be59730ebce071eceaf6bfdb8d3a20e')
    version('0.10.0', '795c5dd192e310ffff38cfd9430d6b29')
    version('0.9.3', '88d667a8ae870d5adeca8cb7d6795442')
    version('0.9.2', '89f63cc4d0100912f4a1f8a9dee63678')

    # Currently only support for c-family and python
    variant('c', default=True,
            description="Build support for C-family languages")
    variant('pic', default=True,
            description='Build position independent code')
    variant('python', default=True,
            description="Build support for python")

    depends_on('pkgconfig', type='build')
    depends_on('java')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('boost@1.53:')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('openssl')

    # Variant dependencies
    extends('python', when='+python')

    depends_on('zlib', when='+c')
    depends_on('libevent', when='+c')

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.append_flags('CFLAGS', self.compiler.pic_flag)
            spack_env.append_flags('CXXFLAGS', self.compiler.pic_flag)

    def install(self, spec, prefix):
        env['PY_PREFIX'] = prefix

        # configure options
        options = ['--prefix=%s' % prefix]

        options.append('--with-boost=%s' % spec['boost'].prefix)
        options.append('--enable-tests=no')

        options.append('--with-nodejs=no')
        options.append('--with-c=%s' % ('yes' if '+c' in spec else 'no'))
        options.append('--with-python=%s' %
                       ('yes' if '+python' in spec else 'no'))
        options.append('--with-java=%s' % ('yes' if '+java' in spec else 'no'))
        options.append('--with-go=%s' % ('yes' if '+go' in spec else 'no'))
        options.append('--with-lua=%s' % ('yes' if '+lua' in spec else 'no'))
        options.append('--with-php=%s' % ('yes' if '+php' in spec else 'no'))
        options.append('--with-qt4=%s' % ('yes' if '+qt4' in spec else 'no'))

        configure(*options)

        make()
        make("install")
