##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Thrift(Package):
    """The Apache Thrift software framework, for scalable cross-language services
    development, combines a software stack with a code generation engine to build
    services that work efficiently and seamlessly between C++, Java, Python, PHP,
    Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk, OCaml
     and Delphi and other languages."""

    homepage = "http://thrift.apache.org"
    url      = "http://apache.mirrors.ionfish.org/thrift/0.9.2/thrift-0.9.2.tar.gz"

    version('0.9.2', '89f63cc4d0100912f4a1f8a9dee63678')

    # Currently only support for c-family and python
    variant('c', default=True, description="Build support for C-family languages")
    variant('python', default=True, description="Build support for python")

    depends_on('jdk')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('boost@1.53:')
    depends_on('bison')
    depends_on('flex')
    depends_on('openssl')

    # Variant dependencies
    extends('python', when='+python')

    depends_on('zlib', when='+c')
    depends_on('libevent', when='+c')

    def install(self, spec, prefix):
        env['PY_PREFIX'] = prefix
        env['JAVA_HOME'] = spec['jdk'].prefix

        # configure options
        options = ['--prefix=%s' % prefix]

        options.append('--with-boost=%s' % spec['boost'].prefix)
        options.append('--enable-tests=no')

        options.append('--with-c=%s' % ('yes' if '+c' in spec else 'no'))
        options.append('--with-python=%s' % ('yes' if '+python' in spec else 'no'))
        options.append('--with-java=%s' % ('yes' if '+java' in spec else 'no'))
        options.append('--with-go=%s' % ('yes' if '+go' in spec else 'no'))
        options.append('--with-lua=%s' % ('yes' if '+lua' in spec else 'no'))
        options.append('--with-php=%s' % ('yes' if '+php' in spec else 'no'))
        options.append('--with-qt4=%s' % ('yes' if '+qt4' in spec else 'no'))

        configure(*options)

        make()
        make("install")
